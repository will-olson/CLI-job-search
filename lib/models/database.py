import sqlite3
import json
import os

class Database:
    @staticmethod
    def connect():
        return sqlite3.connect('companies.db')

def is_database_initialized():
    conn = Database.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='companies'")
    result = cursor.fetchone()
    conn.close()
    return result is not None

def load_data_from_json():
    if not os.path.exists('db.json'):
        print("No initial data file found.")
        return {}
    with open('db.json', 'r') as file:
        data = json.load(file)
        return data

def insert_data(cursor, data):
    category_ids = {}
    for category in data.keys():
        cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category,))
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category,))
        category_ids[category] = cursor.fetchone()[0]

    for category, companies in data.items():
        category_id = category_ids[category]
        for company in companies:
            cursor.execute('''
            INSERT OR IGNORE INTO companies (name, link, indeed, favorite, category_id)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                company.get('name'),
                company.get('link'),
                company.get('indeed'),
                int(company.get('favorite', 0)),
                category_id
            ))

def initialize_database():
    conn = Database.connect()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        link TEXT,
        indeed TEXT,
        favorite BOOLEAN,
        category_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        company_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(company_id) REFERENCES companies(id)
    )
    ''')

    if not is_database_initialized():
        data = load_data_from_json()
        insert_data(cursor, data)

    conn.commit()
    conn.close()

initialize_database()