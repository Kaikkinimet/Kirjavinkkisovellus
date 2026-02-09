
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    description TEXT,
    rate INTEGER,
    user_id INTEGER REFERENCES users(id),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    title TEXT,
    value TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    images BLOB
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    rate INTEGER,
    comment TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (item_id, user_id)
);

CREATE INDEX idx_comments_item_id ON comments (item_id);
CREATE INDEX idx_items_user_id ON items (user_id);
CREATE INDEX idx_item_classes_item_id ON item_classes (item_id);
CREATE INDEX idx_comments_user_id ON comments (user_id);
CREATE INDEX idx_items_title ON items (title);
CREATE INDEX idx_items_author ON items (author);
