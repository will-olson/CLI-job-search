from models.database import Database
from models.category import Category

class Company:
    def __init__(self, id, name, link=None, indeed=None, favorite=False, category_id=None, validate=True):
        self.id = id
        self.favorite = favorite
        self.category_id = category_id
        self.name = name

        if validate:
            self.link = link
            self.indeed = indeed
        else:
            self._link = link
            self._indeed = indeed

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Company name cannot be empty.")
        self._name = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        if value and not value.startswith("https://www.linkedin.com/company/"):
            raise ValueError("Link must start with 'https://www.linkedin.com/company/'.")
        self._link = value

    @property
    def indeed(self):
        return self._indeed

    @indeed.setter
    def indeed(self, value):
        if value and not value.startswith("https://www.indeed.com/cmp/"):
            raise ValueError("Indeed link must start with 'https://www.indeed.com/cmp/'.")
        self._indeed = value

    @classmethod
    def create(cls, name, link, indeed, favorite, category_name):
        try:
            category_id = Category.get_or_create(category_name)
            temp_company = cls(id=None, name=name, link=link, indeed=indeed, favorite=favorite, category_id=category_id, validate=True)
        except ValueError as e:
            print(f"Validation error: {e}")
            return None

        if cls.find_by_name(name):
            print(f"Company '{name}' already exists.")
            return None

        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO companies (name, link, indeed, favorite, category_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, link, indeed, favorite, category_id))
        conn.commit()
        conn.close()

        return cls(id=cursor.lastrowid, name=name, link=link, indeed=indeed, favorite=favorite, category_id=category_id, validate=True)

    @classmethod
    def get_all(cls):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, link, indeed, favorite, category_id FROM companies')
        companies = cursor.fetchall()
        conn.close()
        valid_companies = []
        for data in companies:
            try:
                company = cls(*data, validate=False)
                valid_companies.append(company)
            except ValueError as e:
                print(f"Skipping company due to data error: {e}")
        return valid_companies

    @classmethod
    def find_by_name(cls, name):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, link, indeed, favorite, category_id FROM companies WHERE name = ?', (name,))
        company = cursor.fetchone()
        conn.close()
        if company:
            try:
                return cls(*company, validate=False)
            except ValueError as e:
                print(f"Data error when retrieving company '{name}': {e}")
                return None
        return None

    @classmethod
    def find_by_id(cls, company_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, link, indeed, favorite, category_id FROM companies WHERE id = ?', (company_id,))
        company = cursor.fetchone()
        conn.close()
        if company:
            try:
                return cls(*company, validate=False)
            except ValueError as e:
                print(f"Data error when retrieving company with ID '{company_id}': {e}")
                return None
        return None

    def delete(self):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM companies WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()