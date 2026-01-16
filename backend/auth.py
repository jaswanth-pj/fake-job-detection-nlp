from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from datetime import datetime

# 🔐 ONLY THIS EMAIL IS ADMIN
ADMIN_EMAIL = "jaswanth@gmail.com"   # <-- put your real gmail

# -------------------------
# Signup (USER ONLY)
# -------------------------
def signup():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = generate_password_hash(data["password"])

    # 🔒 FORCE USER ROLE AT SIGNUP
    role = "user"

    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            (username, email, password, role)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Signup successful"})

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# -------------------------
# Login (ADMIN LOGIC HERE)
# -------------------------
def login():
    
    data = request.json
    email = data["email"]
    password = data["password"]

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
     ).fetchone()

    if not user or not check_password_hash(user["password"], password):
        conn.close()
        return jsonify({"message": "Invalid credentials"}), 401

    # ✅ ROLE COMES FROM DATABASE (NOT HARD-CODED)
    role = user["role"]

    # 🔐 OPTIONAL: ensure first admin exists
    if email == ADMIN_EMAIL and role != "admin":
        role = "admin"
        conn.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (role, user["id"])
        )

    # Update last login only
    conn.execute(
        "UPDATE users SET last_login = ? WHERE id = ?",
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user["id"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Login successful",
        "user_id": user["id"],
        "email": email,
        "role": role
    })
