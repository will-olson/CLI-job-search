class Company:
    def __init__(self, id, name, link, indeed, favorite, category=None):
        self.id = id
        self.name = name
        self.link = link
        self.indeed = indeed
        self.favorite = favorite
        self.category = category