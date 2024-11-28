import uuid
from models.company import Company
from models.category import Category
from models.user import User
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
            return User.create(choice)

def fetch_news_for_company(company_name, desired_article_count=5):
    current_time = time.time()

    if company_name in news_cache:
        cached_data, timestamp = news_cache[company_name]
        if current_time - timestamp < CACHE_TTL:
            valid_articles = [article for article in cached_data if article['title'] != '[Removed]']
            return valid_articles[:desired_article_count]

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        news_cache[company_name] = (articles, current_time)
        valid_articles = [article for article in articles if article['title'] != '[Removed]']
        return valid_articles[:desired_article_count]
    else:
        print(f"Failed to fetch news for {company_name}: {response.status_code}")
        return []

def list_all_companies():
    companies = Company.get_all()

    if not companies:
        print("\nNo companies available.")
    else:
        print("\nAll Companies:")
        for company in companies:
            print(f"Name: {company.name}, Category: {company.category}")

def add_new_company():
    while True:
        try:
            id = str(uuid.uuid4())[:8]
            name = input("Enter Name: ").strip()
            link = input("Enter LinkedIn URL: ").strip()
            indeed = input("Enter Indeed URL: ").strip()
            category = input("Enter Category: ").strip()

            company = Company.create(id, name, link, indeed, False, category)
            if company:
                print(f"Company '{company.name}' added successfully.")
            break

        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def delete_company():
    company_name = input("Enter the name of the company to delete: ").strip()
    company = Company.find_by_name(company_name)

    if company:
        try:
            company.delete()
            print(f"Company '{company_name}' deleted.")
        except Exception as e:
            print(f"An error occurred while deleting the company: {e}")
    else:
        print(f"Company '{company_name}' not found or data error.")

def view_companies_in_category_and_news(category_name):
    category = Category(category_name)
    companies = category.get_companies()

    if companies:
        print(f"\nCompanies in '{category_name}':")
        for company in companies:
            print(f"Name: {company.name}, LinkedIn: {company.link}, Indeed: {company.indeed}")
            articles = fetch_news_for_company(company.name)
            if articles:
                print(f"\nArticles for {company.name}:")
                for article in articles[:5]:
                    print(f"- {article['title']} ({article['source']['name']})")
                    print(f"  {article['url']}\n")
            else:
                print(f"No recent articles for {company.name}.")
    else:
        print(f"No companies found in the category '{category_name}'.")

def view_categories_and_news():
    categories = Category.get_all()

    print("\nCategories:")
    for category in categories:
        print(f"- {category.name}")

    category_name = input("Enter a category name to view companies and news, or press Enter to go back: ").strip()
    if category_name:
        view_companies_in_category_and_news(category_name)

def view_favorites(user):
    favorites = user.get_favorites()

    print(f"\nFavorite Companies for {user.name}:")
    for company in favorites:
        print(f"Company: {company.name}, LinkedIn: {company.link}, Indeed: {company.indeed}")
        articles = fetch_news_for_company(company.name)
        if articles:
            print(f"\nArticles for {company.name}:")
            for article in articles[:5]:
                print(f"- {article['title']} ({article['source']['name']})")
                print(f"  {article['url']}\n")
        else:
            print(f"No recent articles for {company.name}.")

def favorite_company(user):
    company_name = input("Enter the name of the company to favorite: ")
    company = Company.find_by_name(company_name)

    if company:
        company.add_favorite(user)
        print(f"Company '{company_name}' marked as favorite for {user.name}.")
    else:
        print(f"Company '{company_name}' not found.")

def unfavorite_company(user):
    company_name = input("Enter the name of the company to unfavorite: ")
    company = Company.find_by_name(company_name)

    if company:
        company.remove_favorite(user)
        print(f"Company '{company_name}' unfavorited for {user.name}.")
    else:
        print(f"Company '{company_name}' is not in your favorites.")

def delete_user(current_user):
    user_name = input("Enter the name of the user to delete: ").strip()
    user = User.find_by_name(user_name)

    if user:
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