from . import Database

class Company:
    def __init__(self, id, name, link=None, indeed=None, favorite=False, category=None, validate=True):
        self.id = id
        self._name = None
        self._link = None
        self._indeed = None
        self.favorite = favorite
        self.category = category
        self.name = name

        # Perform validation for new companies
        if validate:
            self.link = link
            self.indeed = indeed
        else:
            # Bypass validation for existing companies
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
    def create(cls, id, name, link, indeed, favorite, category):
        if cls.find_by_name(name):
            print(f"Company '{name}' already exists.")
            return None
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO companies (id, name, link, indeed, favorite, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, name, link, indeed, favorite, category))
        conn.commit()
        conn.close()
        return cls(id=id, name=name, link=link, indeed=indeed, favorite=favorite, category=category, validate=True)

    @classmethod
    def get_all(cls):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM companies')
        companies = cursor.fetchall()
        conn.close()
        valid_companies = []
        for data in companies:
            try:
                company = cls(*data, validate=False)  # Bypass validation for existing data
                valid_companies.append(company)
            except ValueError as e:
                print(f"Skipping company due to data error: {e}")
        return valid_companies

    @classmethod
    def find_by_name(cls, name):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM companies WHERE name = ?', (name,))
        company = cursor.fetchone()
        conn.close()
        if company:
            try:
                return cls(*company, validate=False)  # Bypass validation for existing data
            except ValueError as e:
                print(f"Data error when retrieving company '{name}': {e}")
                return None
        return None

    @classmethod
    def find_by_id(cls, company_id):
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM companies WHERE id = ?', (company_id,))
        company = cursor.fetchone()
        conn.close()
        if company:
            try:
                return cls(*company, validate=False)  # Bypass validation for existing data
            except ValueError as e:
                print(f"Data error when retrieving company with ID '{company_id}': {e}")
                return None
        return None

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