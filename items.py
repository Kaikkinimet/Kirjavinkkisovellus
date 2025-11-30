import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    reslut = db.query(sql)

    classes = {}
    for title, value in reslut:
        classes[title] = []
    for title, value in reslut:
        classes[title].append(value)
    return classes


def add_item(title, author, description, rate, user_id, classes):
    sql = """INSERT INTO items (title, author, description, rate, user_id) 
               VALUES (?, ?, ?, ?, ?)"""
    item_id = db.execute(sql, [title, author, description, rate, user_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])
    return item_id



def add_class(item_id, title, value):
    sql = """INSERT INTO item_classes (item_id, title, value)
             VALUES (?, ?, ?)"""
    db.execute(sql, [item_id, title, value])

def get_classes(item_id):
    sql = """SELECT title, value 
            FROM item_classes 
            WHERE item_id = ?"""
    return db.query(sql, [item_id])
    

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)


def get_item(item_id):
    sql = """
        SELECT 
            items.id,
            items.title,
            items.author,
            items.description,
            items.rate,
            items.user_id,
            users.username
        FROM items
        JOIN users ON items.user_id = users.id
        WHERE items.id = ?
    """
    result = db.query(sql, [item_id])
    return result[0] if result else None


def update_item(item_id, title, author, description, rate, classes):
    sql = """
        UPDATE items
        SET title = ?, author = ?, description = ?, rate = ?
        WHERE id = ?
    """
    db.execute(sql, [title, author, description, rate, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])


def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """
        SELECT id, title
        FROM items
        WHERE title LIKE ?
        OR author LIKE ?
        OR genre LIKE ?
        OR description LIKE ?
        ORDER BY id DESC
    """
    like = "%" + query + "%"
    return db.query(sql, [like, like, like, like])

