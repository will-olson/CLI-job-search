from helpers import (
    exit_program,
    list_all_companies,
    view_categories_and_news,
    view_favorites,
    add_new_company,
    favorite_company,
    unfavorite_company,
    delete_company,
    delete_user,
    get_user,
)

def main():
    user = get_user()
    while True:
        if user is None:
            user = get_user()

        menu(user)
        choice = input("> ").strip()
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_all_companies()
        elif choice == "2":
            view_categories_and_news()
        elif choice == "3":
            view_favorites(user)
        elif choice == "4":
            add_new_company()
        elif choice == "5":
            favorite_company(user)
        elif choice == "6":
            unfavorite_company(user)
        elif choice == "7":
            delete_company()
        elif choice == "8":
            user = get_user()
        elif choice == "9":
            user = delete_user(user)
        else:
            print("Invalid choice")

def menu(user):
    print(f"\nCurrent User: {user.name}")
    print("Please select an option:")
    print("0. Exit the program")
    print("1. List all companies")
    print("2. View company categories and recent news")
    print("3. View favorite companies")
    print("4. Add a new company")
    print("5. Favorite a company")
    print("6. Unfavorite a company")
    print("7. Delete a company")
    print("8. Change user")
    print("9. Delete user")

if __name__ == "__main__":
    main()