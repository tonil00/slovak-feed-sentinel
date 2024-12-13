# Project Setup

## Overview
This project fetches RSS feeds, processes the data, and stores it in a PostgreSQL database. It uses Python along with Poetry for dependency management to ensure an easy setup and reproducible environment.

---

## Prerequisites

### 1. Install Required Tools
- **Python**: Ensure you have Python 3.8 or later installed.
- **Homebrew** (for macOS): Install Homebrew if not already installed.
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- **Poetry**: Install Poetry for dependency management using Homebrew:
  ```bash
  brew install poetry
  ```

Verify the Poetry installation:
```bash
poetry --version
```

- **PostgreSQL Client**: Ensure you have a PostgreSQL client installed for interacting with the database.
  ```bash
  brew install postgresql
  ```

---

## Setup Steps

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-repo/slovak-feed-sentinel.git
cd slovak-feed-sentinel
```

### 2. Install Dependencies
Use Poetry to install all required dependencies:
```bash
poetry install
```

### 3. Create an `.env` File
Create a `.env` file in the project root directory to store sensitive data, such as database credentials. Example `.env`:
```env
DB_HOST=your-database-host
DB_NAME=your-database-name
DB_USER=your-username
DB_PASSWORD=your-password
```

### 4. Run the Script
To execute the RSS scraper and store data in the database, run:
```bash
poetry run python script.py
```

---

## Support
For any issues or questions, feel free to open an issue on the GitHub repository or contact the project maintainer.

