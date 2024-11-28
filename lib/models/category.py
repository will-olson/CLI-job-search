class Category:
    def __init__(self, name):
        self.name = name
        self.companies = []

    def add_company(self, company):
        self.companies.append(company)