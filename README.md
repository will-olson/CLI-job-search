# CLI Job Search Tool

## Overview

- Welcome to the CLI Job Search Tool for Flatiron students. This application serves as a command-line interface for managing a database of companies, users, and their favorite companies. 

- This tool allows users to add their own profiles while performing various operations such as adding, deleting, and favoriting companies.  

- There is an API integration to fetch recent news articles for favorited companies and those shown in the industry categories section.

---

## Features

**User Management:** Create, delete, and switch between user profiles.

**Company Management:** Add, view, and delete companies with input validation for new entries.

**Favorite Management:** Mark companies as favorites and manage these relationships.

**Category Exploration:** Explore companies by category and view related news.

**News Integration:** Fetch news articles related to companies using an external API.

## Installation

Follow these steps to install and set up the application:

### I. Clone the Repository:
bash
git clone <repository-url>
cd <repository-directory>

### II. Set Up the Environment:
Ensure you have Pipenv installed. If not, install it via pip:
bash
pip install pipenv

### III. Install Dependencies:
Use Pipenv to install the required packages as specified in the Pipfile:
bash
pipenv install

### IV. Activate the Virtual Environment:
Activate the Pipenv virtual environment:
bash
pipenv shell

### V. Running the Application
Navigate to the lib Directory:
Ensure you're in the lib directory where cli.py resides:
bash
cd lib

### VI. Launch the CLI Application:
Run the application using the python command:
bash
python cli.py

### VII. Directory Structure
Here's a quick overview of the key directories and files:

```python
<root-directory>/
│
├── Pipfile
└── lib/
    ├── cli.py              # Main CLI interface
    ├── helpers.py          # Helper functions for CLI operations
    ├── db.json             # JSON file with initial data
    ├── models/
    │   ├── __init__.py     # Database initialization and setup
    │   ├── category.py     # Category model and logic
    │   ├── company.py      # Company model and logic
    │   └── user.py         # User model and logic
```

### VIII. Usage Examples
- Add a New User: Follow the prompts in the CLI to create a new user profile.

- Add a New Company: Select the option to add a company, then provide details such as name, LinkedIn URL, Indeed URL, and category. Note that the Linkedin and Indeed links must follow a key format.

- View All Companies:Choose the option to list all companies and view their details.

- Favorite a Company: Select a 'Favorite a company' from the main and enter its name. This will only favorite the company for the current user. 

- View favorites: This will option (3) on the menu will show all companies favorited for a given user along with the corresponding Linkedin & Indeed links and 5 recent news articles per company.

- Explore Categories: View available categories and select one to explore companies and related news.
