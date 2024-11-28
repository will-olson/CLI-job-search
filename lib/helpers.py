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

def view_companies_in_category_and_news(category_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name, link, indeed FROM companies WHERE category = ?', (category_name,))
    companies = cursor.fetchall()
    conn.close()

    if companies:
        print(f"\nCompanies in '{category_name}':")
        for company in companies:
            company_name, linkedin_link, indeed_link = company
            print(f"Name: {company_name}, LinkedIn: {linkedin_link}, Indeed: {indeed_link}")
            # Fetch news for each company
            articles = fetch_news_for_company(company_name)
            if articles:
                print(f"\nArticles for {company_name}:")
                for article in articles[:5]:
                    print(f"- {article['title']} ({article['source']['name']})")
                    print(f"  {article['url']}\n")
            else:
                print(f"No recent articles for {company_name}.")
    else:
        print(f"No companies found in the category '{category_name}'.")

def view_categories_and_news():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM companies')
    categories = cursor.fetchall()
    conn.close()

    category_objects = [Category(category[0]) for category in categories]

    print("\nCategories:")
    for category in category_objects:
        print(f"- {category.name}")

    category_name = input("Enter a category name to view companies and news, or press Enter to go back: ").strip()
    if category_name:
        view_companies_in_category_and_news(category_name)

def view_favorites(user):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT companies.name, companies.link, companies.indeed
    FROM favorites
    JOIN companies ON favorites.company_id = companies.id
    WHERE favorites.user_id = ?
    ''', (user.id,))
    user_favorites = cursor.fetchall()

    # Fetch all favorites across users
    cursor.execute('''
    SELECT users.name AS user_name, companies.name, companies.link, companies.indeed
    FROM favorites
    JOIN users ON favorites.user_id = users.id
    JOIN companies ON favorites.company_id = companies.id
    ''')
    all_favorites = cursor.fetchall()
    conn.close()

    print(f"\nFavorite Companies for {user.name}:")
    for favorite in user_favorites:
        company_name, linkedin_link, indeed_link = favorite
        print(f"Company: {company_name}, LinkedIn: {linkedin_link}, Indeed: {indeed_link}")
        # Fetch news for each favorite company
        articles = fetch_news_for_company(company_name)
        if articles:
            print(f"\nArticles for {company_name}:")
            for article in articles[:5]:
                print(f"- {article['title']} ({article['source']['name']})")
                print(f"  {article['url']}\n")
        else:
            print(f"No recent articles for {company_name}.")

    print("\nAll Favorited Companies Across Users:")
    for favorite in all_favorites:
        user_name, company_name, linkedin_link, indeed_link = favorite
        print(f"User: {user_name}, Company: {company_name}, LinkedIn: {linkedin_link}, Indeed: {indeed_link}")

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