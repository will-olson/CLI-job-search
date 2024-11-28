from . import Database

class Company:
    def __init__(self, id, name, link=None, indeed=None, favorite=False, category=None):
        self.id = id
        self.name = name
        self.link = link
        self.indeed = indeed
        self.favorite = favorite
        self.category = category

    @classmethod
    def create(cls, id, name, link, indeed, favorite, category):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO companies (id, name, link, indeed, favorite, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, name, link, indeed, favorite, category))
        conn.commit()
        conn.close()
        return cls(id=id, name=name, link=link, indeed=indeed, favorite=favorite, category=category)

    @classmethod
    def get_all(cls):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM companies')
        companies = cursor.fetchall()
        conn.close()
        return [cls(*company) for company in companies]

    @classmethod
    def find_by_id(cls, company_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM companies WHERE id = ?', (company_id,))
        company = cursor.fetchone()
        conn.close()
        return cls(*company) if company else None
    
    @classmethod
    def find_by_name(cls, name):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM companies WHERE name = ?', (name,))
        company = cursor.fetchone()
        conn.close()
        return cls(*company) if company else None

    def add_favorite(self, user):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO favorites (user_id, company_id)
            VALUES (?, ?)
        ''', (user.id, self.id))
        conn.commit()
        conn.close()

    def remove_favorite(self, user):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM favorites WHERE user_id = ? AND company_id = ?', (user.id, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM companies WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()
