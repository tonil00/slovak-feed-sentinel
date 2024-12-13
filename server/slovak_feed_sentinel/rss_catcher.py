import os
from dotenv import load_dotenv
import requests
import feedparser
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress the warning
warnings.simplefilter('ignore', InsecureRequestWarning)

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Define RSS feeds
rss_feeds = {
    "Aktuality.sk": "https://www.aktuality.sk/rss/",
    "SME.sk": "https://www.sme.sk/rss",
    "DenníkN": "https://dennikn.sk/feed/",
    "Pravda.sk": "https://www.spravy.pravda.sk/rss/xml/",
    "HN Online": "https://www.hnonline.sk/rss"
}

# Function to connect to PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to insert articles into PostgreSQL
def insert_articles_to_db(articles):
    conn = connect_to_db()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # Ensure the articles table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id SERIAL PRIMARY KEY,
                    source VARCHAR(255),
                    title TEXT,
                    link TEXT UNIQUE,
                    published TIMESTAMP,
                    summary TEXT,
                    category TEXT
                )
            """)

            # Insert new articles
            insert_query = """
                INSERT INTO articles (source, title, link, published, summary, category)
                VALUES %s
                ON CONFLICT (link) DO NOTHING
            """
            values = [
                (
                    article["Source"],
                    article["Title"],
                    article["Link"],
                    datetime.strptime(article["Published"], "%a, %d %b %Y %H:%M:%S %z") if article["Published"] else None,
                    article["Summary"],
                    article["Category"]
                )
                for article in articles
            ]
            execute_values(cur, insert_query, values)
            conn.commit()
            print(f"Inserted {len(values)} new articles.")
    except Exception as e:
        print(f"Error inserting articles: {e}")
    finally:
        conn.close()

# Fetch and process RSS feeds
def fetch_rss_feeds():
    articles = []
    for source, url in rss_feeds.items():
        try:
            # Fetch RSS feed content with SSL verification disabled
            response = requests.get(url, verify=False)
            response.raise_for_status()
            feed = feedparser.parse(response.content)

            print(f"Fetched RSS feed from {source}")

            for entry in feed.entries:
                category = entry.get("category", "Unknown")  # Get the category if available
                articles.append({
                    "Source": source,
                    "Title": entry.title,
                    "Link": entry.link,
                    "Published": entry.published if "published" in entry else None,
                    "Summary": entry.summary if "summary" in entry else None,
                    "Category": category
                })
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch RSS feed from {source}: {e}")
    return articles

# Define the main function
def main():
    articles = fetch_rss_feeds()
    insert_articles_to_db(articles)

# Entry point for the script
if __name__ == "__main__":
    main()
