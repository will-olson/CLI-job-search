# helpers.py

import sqlite3
import uuid
from models.company import Company
from models.category import Category
from models.user import User
import requests

NEWS_API_KEY = "01376e4cfa834ceabaeac2a7025c77a5"

def connect_db():
    return sqlite3.connect('companies.db')

def get_user():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    print("\nExisting Users:")
    user_dict = {str(user[0]): user[1] for user in users}
    for id_str, name in user_dict.items():
        print(f"{id_str}. {name}")

    while True:
        choice = input("Select a user by ID (1, 2, 3, etc) or enter a new user's name: ").strip()

        if choice in user_dict:
            print(f"Logged in as {user_dict[choice]}.")
            return User(int(choice), user_dict[choice])
        else:
            # Treat any non-integer input as a new user name
            return create_new_user(choice)

def create_new_user(name=None):
    if not name:
        name = input("Enter the new user's name: ").strip()

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        print(f"User '{name}' created successfully.")
        return User(user_id, name)
    except sqlite3.IntegrityError:
        print(f"User '{name}' already exists. Please choose a different name.")
        return get_user()

def fetch_news_for_company(company_name):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    else:
        print(f"Failed to fetch news for {company_name}: {response.status_code}")
        return []

def display_company_news():
    company_names = get_company_names()
    for company_name in company_names:
        print(f"\nArticles for {company_name}:")
        articles = fetch_news_for_company(company_name)
        for article in articles[:5]:
            print(f"- {article['title']} ({article['source']['name']})")
            print(f"  {article['url']}\n")

def get_company_names():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM companies')
    companies = cursor.fetchall()
    conn.close()
    return [company[0] for company in companies]

def list_all_companies():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM companies')
    companies = cursor.fetchall()
    conn.close()

    company_objects = [Company(*company) for company in companies]

    print("\nAll Companies:")
    for company in company_objects:
        print(f"Name: {company.name}, Category: {company.category}")

def view_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM companies')
    categories = cursor.fetchall()
    conn.close()

    category_objects = [Category(category[0]) for category in categories]

    print("\nCategories:")
    for category in category_objects:
        print(f"- {category.name}")

    category_name = input("Enter a category name to view companies, or press Enter to go back: ").strip()
    if category_name:
        view_companies_in_category(category_name)

def view_companies_in_category(category_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM companies WHERE category = ?', (category_name,))
    companies = cursor.fetchall()
    conn.close()

    if companies:
        print(f"\nCompanies in '{category_name}':")
        for company in companies:
            print(f"Name: {company[1]}, LinkedIn: {company[2]}, Indeed: {company[3]}")
    else:
        print(f"No companies found in the category '{category_name}'.")

def view_favorites(user):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT users.name AS user_name, companies.name AS company_name, companies.link AS linkedin_link, companies.indeed AS indeed_link
    FROM favorites
    JOIN users ON favorites.user_id = users.id
    JOIN companies ON favorites.company_id = companies.id
    WHERE favorites.user_id = ?
    ''', (user.id,))
    user_favorites = cursor.fetchall()

    # Fetch all favorites across users
    cursor.execute('''
    SELECT users.name AS user_name, companies.name AS company_name, companies.link AS linkedin_link, companies.indeed AS indeed_link
    FROM favorites
    JOIN users ON favorites.user_id = users.id
    JOIN companies ON favorites.company_id = companies.id
    ''')
    all_favorites = cursor.fetchall()
    conn.close()

    print(f"\nFavorite Companies for {user.name}:")
    for favorite in user_favorites:
        print(f"Company: {favorite[1]}, LinkedIn: {favorite[2]}, Indeed: {favorite[3]}")

    print("\nAll Favorited Companies Across Users:")
    for favorite in all_favorites:
        print(f"User: {favorite[0]}, Company: {favorite[1]}, LinkedIn: {favorite[2]}, Indeed: {favorite[3]}")

def add_new_company():
    conn = connect_db()
    cursor = conn.cursor()

    id = str(uuid.uuid4())[:8]
    name = input("Enter Name: ")
    link = input("Enter LinkedIn URL: ")
    indeed = input("Enter Indeed URL: ")
    category = input("Enter Category: ")

    cursor.execute('''
    INSERT INTO companies (id, name, link, indeed, category)
    VALUES (?, ?, ?, ?, ?)
    ''', (id, name, link, indeed, category))

    conn.commit()
    conn.close()
    print(f"Company '{name}' added successfully.")

def favorite_company(user):
    company_name = input("Enter the name of the company to favorite: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM companies WHERE name = ?', (company_name,))
    company = cursor.fetchone()

    if company:
        cursor.execute('''
        INSERT OR IGNORE INTO favorites (user_id, company_id)
        VALUES (?, ?)
        ''', (user.id, company[0]))
        conn.commit()
        print(f"Company '{company_name}' marked as favorite for {user.name}.")
    else:
        print(f"Company '{company_name}' not found.")
    conn.close()

def unfavorite_company(user):
    company_name = input("Enter the name of the company to unfavorite: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT companies.id FROM companies
    JOIN favorites ON companies.id = favorites.company_id
    WHERE companies.name = ? AND favorites.user_id = ?
    ''', (company_name, user.id))
    company = cursor.fetchone()

    if company:
        cursor.execute('DELETE FROM favorites WHERE company_id = ? AND user_id = ?', (company[0], user.id))
        conn.commit()
        print(f"Company '{company_name}' unfavorited for {user.name}.")
    else:
        print(f"Company '{company_name}' is not in your favorites.")
    conn.close()

def delete_company():
    company_name = input("Enter the name of the company to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM companies WHERE name = ?', (company_name,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"Company '{company_name}' deleted.")
    else:
        print(f"Company '{company_name}' not found.")
    conn.close()

def exit_program():
    print("Goodbye!")
    exit()