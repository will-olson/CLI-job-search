from . import Database
from .company import Company

class Category:
    def __init__(self, name):
        self.name = name

    @classmethod
    def get_all(cls):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM companies')
        categories = cursor.fetchall()
        conn.close()
        return [cls(category[0]) for category in categories]

    def get_companies(self):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM companies WHERE category = ?', (self.name,))
        companies = cursor.fetchall()
        conn.close()
        return [Company(*company) for company in companies]