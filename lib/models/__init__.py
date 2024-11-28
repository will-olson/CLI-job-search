import sqlite3
import json

class Database:
    @staticmethod
    def connect():
        return sqlite3.connect('companies.db')

CONN = Database.connect()
CURSOR = CONN.cursor()

CURSOR.execute('''
CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    link TEXT,
    indeed TEXT,
    favorite BOOLEAN,
    category TEXT
)
''')

CURSOR.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

CURSOR.execute('''
CREATE TABLE IF NOT EXISTS favorites (
    user_id INTEGER,
    company_id TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(company_id) REFERENCES companies(id),
    PRIMARY KEY (user_id, company_id)
)
''')

def load_data_from_json():
    with open('db.json', 'r') as file:
        data = json.load(file)
        return data

def insert_data(data):
    for category, companies in data.items():
        for company in companies:
            CURSOR.execute('''
            INSERT OR IGNORE INTO companies (id, name, link, indeed, favorite, category)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                company.get('id'),
                company.get('name'),
                company.get('link'),
                company.get('indeed'),
                int(company.get('favorite', 0)),
                company.get('category', category)
            ))

data = load_data_from_json()
insert_data(data)

CONN.commit()
CONN.close()