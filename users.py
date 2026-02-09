import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    try:
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return False
    return True

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]

    if check_password_hash(password_hash, password):
        return user_id
    return None

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    rows = db.query(sql, [user_id])
    return rows[0] if rows else None

def get_items(user_id):
    sql = "SELECT id, title FROM items WHERE user_id = ? ORDER BY title COLLATE NOCASE"
    return db.query(sql, [user_id])
