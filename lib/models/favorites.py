from . import Database
from .company import Company

class Favorites:
    @staticmethod
    def add_favorite(user_id, company_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO favorites (user_id, company_id)
            VALUES (?, ?)
        ''', (user_id, company_id))
        conn.commit()
        conn.close()

    @staticmethod
    def remove_favorite(user_id, company_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM favorites WHERE user_id = ? AND company_id = ?', (user_id, company_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_favorites(user_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT companies.id, companies.name, companies.link, companies.indeed, companies.favorite, companies.category
            FROM favorites
            JOIN companies ON favorites.company_id = companies.id
            WHERE favorites.user_id = ?
        ''', (user_id,))
        favorites = cursor.fetchall()
        conn.close()
        return [Company(*company) for company in favorites]