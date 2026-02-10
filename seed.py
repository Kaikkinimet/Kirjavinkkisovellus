
import random
import sqlite3

USER_COUNT = 1000
ITEM_COUNT = 10**5
CLASSES = {
    "Osasto": ["Aikuiset", "Nuoret", "Lapset"],
    "Laji": ["Romaani", "Jännitys", "Kauhu", "Muu"],
}

def main():
    db = sqlite3.connect("database.db")
    db.execute("DELETE FROM item_classes")
    db.execute("DELETE FROM images")
    db.execute("DELETE FROM items")
    db.execute("DELETE FROM classes")
    db.execute("DELETE FROM users")
    for i in range(1, USER_COUNT + 1):
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("user" + str(i), "seed_hash"),
        )
    for title, values in CLASSES.items():
        for value in values:
            db.execute(
                "INSERT INTO classes (title, value) VALUES (?, ?)",
                (title, value),
            )
    for i in range(1, ITEM_COUNT + 1):
        title = "title" + str(i)
        author = "author" + str(random.randint(1, USER_COUNT))
        description = "description" + str(i)
        rate = random.randint(1, 5)
        user_id = random.randint(1, USER_COUNT)
        db.execute(
            """INSERT INTO items (title, author, description, rate, user_id, created_at)
               VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (title, author, description, rate, user_id),
        )
    for item_id in range(1, ITEM_COUNT + 1):
        for title, values in CLASSES.items():
            value = random.choice(values)
            db.execute(
                "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)",
                (item_id, title, value),
            )
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
