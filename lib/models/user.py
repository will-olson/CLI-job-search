from . import Database
from .company import Company
import sqlite3

class User:
    def __init__(self, id=None, name=None):
        self.id = id
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("User name cannot be empty.")
        self._name = value

    @classmethod
    def create(cls, name):
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return cls(id=user_id, name=name)
        except sqlite3.IntegrityError:
            conn.close()
            print("User already exists. Enter a new name.")
            return None

    @classmethod
    def find_by_id(cls, user_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return cls(id=user[0], name=user[1]) if user else None

    @classmethod
    def find_by_name(cls, name):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
        user = cursor.fetchone()
        conn.close()
        return cls(id=user[0], name=user[1]) if user else None

    @classmethod
    def get_all(cls):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        return [cls(id=user[0], name=user[1]) for user in users]

    def delete(self):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()

    def confirm_and_delete(self):
        confirm = input(f"Are you sure you want to delete your profile '{self.name}'? This will log you out. (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.delete()
            print(f"User '{self.name}' deleted.")
            return True
        print(f"User '{self.name}' deletion cancelled.")
        return False

    def get_favorites(self):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT companies.id, companies.name, companies.link, companies.indeed, companies.favorite, companies.category
            FROM favorites
            JOIN companies ON favorites.company_id = companies.id
            WHERE favorites.user_id = ?
        ''', (self.id,))
        favorites = cursor.fetchall()
        conn.close()
        return [Company(*company) for company in favorites]