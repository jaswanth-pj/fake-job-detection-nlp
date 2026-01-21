from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from datetime import datetime


ADMIN_EMAIL = "jaswanth@gmail.com"  


def signup():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = generate_password_hash(data["password"])

  
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

   
    role = user["role"]

    
    if email == ADMIN_EMAIL and role != "admin":
        role = "admin"
        conn.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (role, user["id"])
        )


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
