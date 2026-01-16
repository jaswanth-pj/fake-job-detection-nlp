from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import pickle
import re
import uuid
import os
from datetime import datetime
import subprocess
from auth import signup, login
from database import create_tables, get_db_connection
from ocr_utils import extract_text_from_image
app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:5174"]}},
    supports_credentials=True
)

create_tables()

vectorizer = pickle.load(open("./model/tfidf_vectorizer.pkl", "rb"))
logistic_model = pickle.load(open("./model/logistic_model.pkl", "rb"))


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    return text

SCAM_KEYWORDS = [
    "telegram",
    "whatsapp",
    "no interview",
    "pan card",
    "aadhaar",
    "bank details",
    "verification fee",
    "registration fee",
    "pay fee",
    "immediate joining",
    "contact hr directly"
]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("text")
    user_id = request.json.get("user_id")

    if not data or not user_id:
        return jsonify({"error": "text or user_id missing"}), 400

    text_lower = data.lower()

   
    if any(k in text_lower for k in SCAM_KEYWORDS):
        result = "Fake Job"
        label = 1
        confidence = 99.0
    else:
        cleaned = clean_text(data)
        transformed = vectorizer.transform([cleaned])
        proba = logistic_model.predict_proba(transformed)[0]
        label = int(proba.argmax())
        confidence = round(max(proba) * 100, 2)
        result = "Fake Job" if label == 1 else "Real Job"

    conn = get_db_connection()
    cursor = conn.execute("""
        INSERT INTO predictions (user_id, text, result, created_at, flagged)
        VALUES (?, ?, ?, ?, 0)
    """, (
        user_id,
        data,
        result,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "prediction_id": prediction_id,
        "prediction": result,
        "label": label,
        "confidence": confidence
    })

@app.route("/predict-image", methods=["POST"])
def predict_image():
    user_id = request.form.get("user_id")
    file = request.files.get("image")

    if not user_id or not file:
        return jsonify({"error": "user_id or image missing"}), 400

    path = f"temp_{uuid.uuid4().hex}.jpg"
    file.save(path)
    extracted_text = extract_text_from_image(path)
    os.remove(path)

    cleaned = clean_text(extracted_text)
    transformed = vectorizer.transform([cleaned])
    proba = logistic_model.predict_proba(transformed)[0]
    label = int(proba.argmax())
    confidence = round(max(proba) * 100, 2)
    result = "Fake Job" if label == 1 else "Real Job"

    conn = get_db_connection()
    cursor = conn.execute("""
        INSERT INTO predictions (user_id, text, result, created_at, flagged)
        VALUES (?, ?, ?, ?, 0)
    """, (
        user_id,
        extracted_text,
        result,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "prediction_id": prediction_id,
        "extracted_text": extracted_text,
        "prediction": result,
        "label": label,
        "confidence": confidence
    })


@app.route("/admin/flagged")
def admin_flagged_posts():
    conn = get_db_connection()

    rows = conn.execute("""
        SELECT id, user_id, text, result, created_at
        FROM predictions
        WHERE flagged = 1
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()

    return jsonify([
        {
            "id": row["id"],
            "user_id": row["user_id"],
            "text": row["text"][:200] + "...",
            "result": row["result"],
            "created_at": row["created_at"]
        }
        for row in rows
    ])

def get_flagged_count():
    conn = get_db_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE flagged = 1"
    ).fetchone()[0]
    conn.close()
    return count

@app.route("/flag/<int:prediction_id>", methods=["POST"])
def flag_prediction(prediction_id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE predictions SET flagged = 1 WHERE id = ?",
        (prediction_id,)
    )
    conn.commit()
    conn.close()

    flagged_count = get_flagged_count()


    if flagged_count % 5 == 0:
        subprocess.Popen(
            ["python", "model/retrain_model.py"],
            cwd="."
        )

    return jsonify({"message": "Prediction flagged and retraining checked"})


@app.route("/user/dashboard/<int:user_id>")
def user_dashboard(user_id):
    conn = get_db_connection()

    user = conn.execute(
        "SELECT email, last_login FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    total = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE user_id = ?",
        (user_id,)
    ).fetchone()[0]

    fake = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE user_id = ? AND result='Fake Job'",
        (user_id,)
    ).fetchone()[0]

    conn.close()

    return jsonify({
        "email": user["email"],
        "last_login": user["last_login"],
        "total_predictions": total,
        "fake": fake,
        "real": total - fake
    })


@app.route("/user/predictions/<int:user_id>")
def user_predictions(user_id):
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT id, text, result, created_at, flagged
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])

@app.route("/admin/dashboard")
def admin_dashboard():
    conn = get_db_connection()

    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_admins = conn.execute(
        "SELECT COUNT(*) FROM users WHERE role='admin'"
    ).fetchone()[0]
    total_predictions = conn.execute(
        "SELECT COUNT(*) FROM predictions"
    ).fetchone()[0]
    fake_detected = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE result='Fake Job'"
    ).fetchone()[0]
    flagged_posts = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE flagged=1"
    ).fetchone()[0]

    users = conn.execute("""
        SELECT id, email, role, last_login FROM users
    """).fetchall()

    conn.close()

    return jsonify({
        "total_users": total_users,
        "total_admins": total_admins,
        "total_predictions": total_predictions,
        "fake_detected": fake_detected,
        "real_detected": total_predictions - fake_detected,
        "flagged_posts": flagged_posts,
        "users": [dict(u) for u in users]
    })

@app.route("/admin/change-role", methods=["POST", "OPTIONS"])
def change_user_role():
    if request.method == "OPTIONS":
        return "", 200

    data = request.json
    user_id = data.get("user_id")
    role = data.get("role")

    if role not in ["admin", "user"]:
        return jsonify({"error": "Invalid role"}), 400

    conn = get_db_connection()
    conn.execute(
        "UPDATE users SET role = ? WHERE id = ?",
        (role, user_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Role updated successfully"})

@app.route("/admin/export-csv")
def export_csv():
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT p.id, u.email, p.text, p.result, p.created_at, p.flagged
        FROM predictions p JOIN users u ON p.user_id = u.id
    """).fetchall()
    conn.close()

    def generate():
        yield "id,email,text,result,created_at,flagged\n"
        for r in rows:
            yield f'{r["id"]},{r["email"]},"{r["text"]}",{r["result"]},{r["created_at"]},{r["flagged"]}\n'

    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=job_predictions.csv"})


@app.route("/signup", methods=["POST"])
def signup_route():
    return signup()

@app.route("/login", methods=["POST"])
def login_route():
    return login()

# -----------------------
# RUN
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
