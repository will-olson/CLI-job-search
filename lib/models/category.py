from models.database import Database

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def get_all(cls):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        conn.close()
        return [cls(id=category[0], name=category[1]) for category in categories]

    @classmethod
    def get_or_create(cls, name):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM categories WHERE name = ?', (name,))
        category = cursor.fetchone()
        if category:
            category_id = category[0]
        else:
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
            conn.commit()
            category_id = cursor.lastrowid
        conn.close()
        return category_id

    @classmethod
    def get_name_by_id(cls, category_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        conn.close()
        return category[0] if category else "Unknown"

    def get_companies(self):
        from models.company import Company
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, link, indeed, favorite, category_id FROM companies WHERE category_id = ?', (self.id,))
        companies = cursor.fetchall()
        conn.close()
        return [Company(*company, validate=False) for company in companies]