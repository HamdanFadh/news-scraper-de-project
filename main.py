import sqlite3
import random
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta, date
from tqdm import tqdm

def logging(message):
    timestamp = datetime.now()
    log_message = f"{timestamp} - {message}"
    with open("scraper_log.log", "a") as log_file:
        log_file.write(log_message + "\n")


# Create database
def create_database():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS news_articles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            publish_date DATE,
            created_at NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+7 hours'))
        )
        '''
    )

    conn.commit()
    return conn

# Scraping
def scrape_kompas():
    
    today = date.today()
    # Master lists
    all_titles = []
    all_urls = []
    all_pub_dates = []
    page = 1
    pages_scraped = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    while True:  # Keep looping the pages until no articles found
        titles = []
        urls = []
        pub_dates = []
        
        response = requests.get(f'https://indeks.kompas.com/?site=news&date={today}&page={page}', headers = headers)
        response.raise_for_status()  # Check for HTTP errors
        logging(f'Fetching kompas.com: Date {today}, Page {page}')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article titles on target page
        for news_heading in soup.find_all('h2', class_='articleTitle'):
            titles.append(news_heading.get_text(strip=True))
            
        for news_url in soup.find_all('a', class_='article-link', href=True):
            urls.append(news_url['href'])
            
        for published_date in soup.find_all('div', class_='articlePost-date'):
            date_text = published_date.get_text(strip=True)
            formatted_date = datetime.strptime(date_text, '%d/%m/%Y').strftime('%Y-%m-%d')
            pub_dates.append(formatted_date)
        
        # Check if we found any articles on target page
        if not titles:  # If no titles were found, break out the page loop
            logging(f'No more articles for date {today}')
            break
        
        # Add the results to master lists
        all_titles.extend(titles)
        all_urls.extend(urls)
        all_pub_dates.extend(pub_dates)
        
        # Go to next page
        page += 1
    # Set interval 2 seconds
    time.sleep(random.uniform(1,3))
    articles = []
    for i in range(len(all_titles)):
        article = (all_titles[i], all_urls[i], all_pub_dates[i])
        articles.append(article)
    return articles


# Insert to database
def insert_articles(conn, articles):
    cursor = conn.cursor()

    articles_added = 0

    for title, url, pub_date in articles:
        try:
            cursor.execute(
                '''
                INSERT into news_articles (title, url, publish_date) VALUES (?, ?, ?)
                ''',
                (title, url, pub_date)
            )
            articles_added += 1
        except:
            pass
    conn.commit()
    return articles_added


def main():
    # Create database and table
    conn = create_database()
    print('Database and table created successfully.')
    logging("Database and table created successfully.")
    
    # Scrape news articles from Kompas
    print("Scraping news articles from Kompas.com...")
    logging("Scraping news articles from Kompas.com...")
    articles = scrape_kompas()
    print(f"Found {len(articles)} articles.")
    logging(f"Found {len(articles)} articles.")
    
    # Insert articles into database
    if articles:
        added = insert_articles(conn, articles)
        print(f"Added {added} new articles to the database.")
        logging(f"Added {added} new articles to the database.")
    
    # Show some sample data
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news_articles LIMIT 5")
    print("\nSample entries in database:")
    logging("\nSample entries in database:")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Title: {row[1]}, URL: {row[2]}, Date: {row[3]}")
        logging(f"ID: {row[0]}, Title: {row[1]}, URL: {row[2]}, Date: {row[3]}")
    
    conn.close()

if __name__ == "__main__":
    main()