import sqlite3
import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)
    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes

def add_item(title, author, description, rate, user_id, classes): # pylint: disable=too-many-arguments, too-many-positional-arguments

    sql = """INSERT INTO items (title, author, description, rate, user_id, created_at)
               VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)"""
    item_id = db.execute(sql, [title, author, description, rate, user_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])
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

def item_count():
    sql = "SELECT COUNT(*) FROM items"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_items(page, page_size):
    sql = """SELECT
                items.id,
                items.title,
                items.author,
                items.rate,
                items.created_at,
                items.user_id,
                users.username,
                AVG(comments.rate) comment_average,
                COUNT(comments.id) comment_count
            FROM items
            JOIN users ON items.user_id = users.id
            LEFT JOIN comments ON items.id = comments.item_id
               GROUP BY items.id
            ORDER BY items.title COLLATE NOCASE
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])


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


def update_item(item_id, title, author, description, rate, classes): # pylint: disable=too-many-arguments, too-many-positional-arguments
    sql = """
        UPDATE items
        SET title = ?, author = ?, description = ?, rate = ?
        WHERE id = ?
    """
    db.execute(sql, [title, author, description, rate, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    like = "%" + query + "%"
    sql = """
        SELECT DISTINCT items.id, items.title
        FROM items
        LEFT JOIN item_classes ic ON ic.item_id = items.id
        WHERE items.title LIKE ?
           OR items.author LIKE ?
           OR items.description LIKE ?
           OR ic.title LIKE ?
           OR ic.value LIKE ?
        ORDER BY items.id DESC
    """
    return db.query(sql, [like, like, like, like, like])

def create_comment(item_id, user_id, rate, comment):
    sql = "INSERT INTO comments (item_id, user_id, rate, comment) VALUES (?, ?, ?, ?)"
    try:
        db.execute(sql, [item_id, user_id, rate, comment])
    except sqlite3.IntegrityError:
        return False
    return True

def get_comments(item_id):
    sql = """SELECT comments.id comment_id, comment, rate, created_at,
                    users.id user_id, users.username
            FROM comments, users
            WHERE comments.item_id = ? AND comments.user_id = users.id
            ORDER BY created_at DESC
        """
    return db.query(sql, [item_id])

def get_comments_average(item_id):
    sql = "SELECT AVG(rate) FROM comments WHERE item_id = ?"
    result = db.query(sql, [item_id])
    return result[0][0] if result and result[0][0] is not None else None

def get_comment(comment_id):
    sql = """SELECT id, item_id, user_id, rate, comment
             FROM comments
             WHERE id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def update_comment(comment_id, rate, comment):
    sql = "UPDATE comments SET rate = ?, comment = ? WHERE id = ?"
    db.execute(sql, [rate, comment, comment_id])

def get_images(item_id):
    sql = "SELECT id FROM images WHERE item_id =?"
    return db.query(sql, [item_id])

def add_image(item_id, image):
    sql = "INSERT INTO images (item_id, images) VALUES (?, ?)"
    db.execute(sql, [item_id, image])

def get_image(image_id):
    sql = "SELECT images FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None
