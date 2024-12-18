from models.database import Database
from models.company import Company
from models.category import Category
from models.user import User
from models.favorites import Favorites
import requests
import time

NEWS_API_KEY = "01376e4cfa834ceabaeac2a7025c77a5"
news_cache = {}
CACHE_TTL = 86400

def get_user():
    users = User.get_all()
    print("\nExisting Users:")
    user_dict = {str(user.id): user.name for user in users}
    for id_str, name in user_dict.items():
        print(f"{id_str}. {name}")

    while True:
        choice = input("Select a user by ID (1, 2, 3, etc) or enter a new user's name: ").strip()
        if choice in user_dict:
            print(f"Logged in as {user_dict[choice]}.")
            return User.find_by_id(int(choice))
        else:
            new_user = User.create(choice)
            if new_user:
                return new_user

def fetch_news_for_company(company_name, desired_article_count=5):
    current_time = time.time()
    if company_name in news_cache:
        cached_data, timestamp = news_cache[company_name]
        if current_time - timestamp < CACHE_TTL:
            return [article for article in cached_data if article['title'] != '[Removed]'][:desired_article_count]

    response = requests.get("https://newsapi.org/v2/everything", params={
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10
    })

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        news_cache[company_name] = (articles, current_time)
        return [article for article in articles if article['title'] != '[Removed]'][:desired_article_count]
    else:
        print(f"Failed to fetch news for {company_name}: {response.status_code}")
        return []

def list_all_companies():
    companies = Company.get_all()
    if companies:
        print("\nAll Companies:")
        for company in companies:
            category_name = Category.get_name_by_id(company.category_id)
            print(f"Name: {company.name}, Category: {category_name}")
    else:
        print("\nNo companies available.")

def add_new_company():
    print("Enter 'exit' at any prompt to return to the main menu.")
    while True:
        try:
            name = input("Enter Name: ").strip()
            if name.lower() == 'exit':
                return print("Returning to the main menu.")

            link = input("Enter LinkedIn URL: ").strip()
            if link.lower() == 'exit':
                return print("Returning to the main menu.")

            indeed = input("Enter Indeed URL: ").strip()
            if indeed.lower() == 'exit':
                return print("Returning to the main menu.")

            category_name = input("Enter Category: ").strip()
            if category_name.lower() == 'exit':
                return print("Returning to the main menu.")

            if Company.create(name, link, indeed, False, category_name):
                print(f"Company '{name}' added successfully.")
            else:
                print(f"Failed to add company. It may already exist.")
            return

        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def delete_company():
    company_name = input("Enter the name of the company to delete: ").strip()
    if company := Company.find_by_name(company_name):
        try:
            company.delete()
            print(f"Company '{company_name}' deleted.")
        except Exception as e:
            print(f"An error occurred while deleting the company: {e}")
    else:
        print(f"Company '{company_name}' not found or data error.")

def view_companies_in_category_and_news(category_name):
    conn = Database.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
    category_data = cursor.fetchone()
    conn.close()

    if category_data:
        category_id = category_data[0]
        category = Category(id=category_id, name=category_name)
        companies = category.get_companies()

        if companies:
            print(f"\nCompanies in '{category_name}':")
            for company in companies:
                print(f"Name: {company.name}, LinkedIn: {company.link}, Indeed: {company.indeed}")
                if articles := fetch_news_for_company(company.name):
                    print(f"\nArticles for {company.name}:")
                    for article in articles[:5]:
                        print(f"- {article['title']} ({article['source']['name']})")
                        print(f"  {article['url']}\n")
                else:
                    print(f"No recent articles for {company.name}.")
        else:
            print(f"No companies found in the category '{category_name}'.")
    else:
        print(f"Category '{category_name}' not found.")

def view_categories_and_news():
    categories = Category.get_all()
    print("\nCategories:")
    for category in categories:
        print(f"- {category.name}")

    category_name = input("Enter a category name to view companies and news, or press Enter to go back: ").strip()
    if category_name:
        view_companies_in_category_and_news(category_name)

def favorite_company(user):
    company_name = input("Enter the name of the company to favorite: ").strip()
    if company := Company.find_by_name(company_name):
        Favorites.add_favorite(user.id, company.id)
        print(f"Company '{company_name}' marked as favorite for {user.name}.")
    else:
        print(f"Company '{company_name}' not found.")

def unfavorite_company(user):
    company_name = input("Enter the name of the company to unfavorite: ").strip()
    if company := Company.find_by_name(company_name):
        Favorites.remove_favorite(user.id, company.id)
        print(f"Company '{company_name}' unfavorited for {user.name}.")
    else:
        print(f"Company '{company_name}' is not in your favorites.")

def view_favorites(user):
    favorites = Favorites.get_user_favorites(user.id)
    print(f"\nFavorite Companies for {user.name}:")
    for company in favorites:
        print(f"Company: {company.name}, LinkedIn: {company.link}, Indeed: {company.indeed}")
        if articles := fetch_news_for_company(company.name):
            print(f"\nArticles for {company.name}:")
            for article in articles[:5]:
                print(f"- {article['title']} ({article['source']['name']})")
                print(f"  {article['url']}\n")
        else:
            print(f"No recent articles for {company.name}.")

def delete_user(current_user):
    user_name = input("Enter the name of the user to delete: ").strip()
    if user := User.find_by_name(user_name):
        if user_name == current_user.name:
            if user.confirm_and_delete():
                print("You have been logged out as your profile was deleted.")
                return None
        else:
            user.delete()
            print(f"User '{user.name}' deleted.")
    else:
        print(f"User with the name '{user_name}' not found.")
    return current_user

def exit_program():
    print("Goodbye!")
    exit()