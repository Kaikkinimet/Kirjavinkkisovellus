import random
import sqlite3


USER_COUNT = 1000
ITEM_COUNT = 10**5
COMMENT_COUNT = 10**6
BATCH_SIZE = 5000
CLASSES = {
    "Osasto": ["Aikuiset", "Nuoret", "Lapset"],
    "Laji": ["Romaani", "Jännitys", "Kauhu", "Muu"],
}


def batched(iterable, size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def main():
    db = sqlite3.connect("database.db")

    db.execute("DELETE FROM comments")
    db.execute("DELETE FROM item_classes")
    db.execute("DELETE FROM images")
    db.execute("DELETE FROM items")
    db.execute("DELETE FROM classes")
    db.execute("DELETE FROM users")

    users = [("user" + str(i), "seed_hash") for i in range(1, USER_COUNT + 1)]
    for batch in batched(users, BATCH_SIZE):
        db.executemany("INSERT INTO users (username, password_hash) VALUES (?, ?)", batch)

    class_rows = []
    for title, values in CLASSES.items():
        for value in values:
            class_rows.append((title, value))
    for batch in batched(class_rows, BATCH_SIZE):
        db.executemany("INSERT INTO classes (title, value) VALUES (?, ?)", batch)

    items = []
    for i in range(1, ITEM_COUNT + 1):
        title = "title" + str(i)
        author = "author" + str(random.randint(1, USER_COUNT))
        description = "description" + str(i)
        rate = random.randint(1, 5)
        user_id = random.randint(1, USER_COUNT)
        items.append((title, author, description, rate, user_id))
        if len(items) >= BATCH_SIZE:
            db.executemany(
                """INSERT INTO items (title, author, description, rate, user_id, created_at)
                   VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                items,
            )
            items = []
    if items:
        db.executemany(
            """INSERT INTO items (title, author, description, rate, user_id, created_at)
               VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            items,
        )

    item_classes = []
    for item_id in range(1, ITEM_COUNT + 1):
        for title, values in CLASSES.items():
            value = random.choice(values)
            item_classes.append((item_id, title, value))
        if len(item_classes) >= BATCH_SIZE:
            db.executemany(
                "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)",
                item_classes,
            )
            item_classes = []
    if item_classes:
        db.executemany(
            "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)",
            item_classes,
        )

    inserted = 0
    while inserted < COMMENT_COUNT:
        batch = []
        for _ in range(BATCH_SIZE):
            user_id = random.randint(1, USER_COUNT)
            item_id = random.randint(1, ITEM_COUNT)
            rate = random.randint(1, 5)
            comment = "comment" + str(inserted + 1)
            batch.append((item_id, user_id, rate, comment))
        db.executemany(
            """INSERT OR IGNORE INTO comments
               (item_id, user_id, rate, comment, created_at)
               VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            batch,
        )
        inserted += len(batch)

    db.commit()
    db.close()


if __name__ == "__main__":
    main()
