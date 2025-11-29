
from werkzeug.security import check_password_hash, generate_password_hash
import db

def get_user(user_id):
    sql = """
        SELECT id, username
        FROM users
        WHERE id = ?
    """
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = """
        SELECT id, title 
        FROM items
        WHERE user_id = ? ORDER BY id DESC
    """
    return db.query(sql, [user_id])
                    
def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])


def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return "VIRHE: väärä tunnus tai salasana"
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]

    #oma: user_id = result[0][0]         
    #oma: password_hash = result[0][1]  
    
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return "VIRHE: väärä tunnus tai salasana"
    
    #vanha:    session["user_id"] = user_id
    #Vanha:     session["username"] = username
    #vanha    return redirect("/")
    #vanha else:
    #vanha     return "VIRHE: väärä tunnus tai salasana"