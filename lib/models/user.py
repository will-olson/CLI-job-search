from . import Database
from .company import Company

class User:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return cls(id=user_id, name=name)

    @classmethod
    def find_by_id(cls, user_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
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