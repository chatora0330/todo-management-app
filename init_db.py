import sqlite3

from config import Config


conn = sqlite3.connect(Config.DATABASE)

cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS todos;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    
    title TEXT NOT NULL,
    description TEXT,
    
    status TEXT NOT NULL DEFAULT "未着手",
    
    priority TEXT NOT NULL DEFAULT "中",
    
    deadline TEXT,
    
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users (id)
);
""")

conn.commit()
conn.close()

print("データベースを初期化しました。")