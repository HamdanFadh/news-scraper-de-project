# News Scraper

This project is a Python-based web scraper designed to extract news articles from [Kompas.com](https://www.kompas.com/), store them in a SQLite database, and log the scraping process. The scraper collects article titles, URLs, and publication dates, ensuring robust data collection with error handling and logging.

## Disclaimer

This project is intended for **educational and learning purposes only**. It demonstrates web scraping techniques and database management. Users are responsible for ensuring compliance with the terms of service of any website they scrape, including Kompas.com. Unauthorized or excessive scraping may violate website policies or applicable laws. Use this code responsibly and ethically.


## Features

- **Web Scraping**: Scrapes news articles from Kompas.com using BeautifulSoup and Requests.
- **Database Storage**: Stores scraped articles in a SQLite database (`news.db`) with fields for ID, title, URL, publication date, and creation timestamp.
- **Logging**: Logs all scraping activities and errors to a file (`scraper_log.log`) for debugging and monitoring.
- **Randomized Delays**: Implements random delays between requests to avoid overwhelming the target server.
- **Error Handling**: Handles HTTP errors and database insertion conflicts gracefully.

## Prerequisites

Python 3.10+ installed. The required Python libraries can be installed using pip.

### Required Libraries

- `sqlite3`
- `requests`
- `beautifulsoup4`
- `tqdm`
- `python-dateutil`

Install the dependencies using:

```bash
pip install requests beautifulsoup4 tqdm python-dateutil
```

## Project Structure

```
news-scraper/
│
├── scraper.py          # Main script containing the scraping and database logic
├── news.db             # SQLite database (generated after running the script)
├── scraper_log.log     # Log file for scraping activities
├── README.md           # This file
```

## Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/news-scraper.git
   cd news-scraper
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, install the libraries listed in the Prerequisites section.

3. **Run the Scraper**:

   ```bash
   python scraper.py
   ```

   The script will:
   - Create a SQLite database (`news.db`) and table (`news_articles`) if they don't exist.
   - Scrape articles from Kompas.com for the current date.
   - Store the articles in the database.
   - Log all activities to `scraper_log.log`.
   - Display a summary of the scraped articles and sample database entries.

## Database Schema

The `news_articles` table in `news.db` has the following schema:

| Column        | Type    | Description                                      |
|---------------|---------|--------------------------------------------------|
| `id`          | INTEGER | Primary key, auto-incremented                   |
| `title`       | TEXT    | Article title (not null)                        |
| `url`         | TEXT    | Article URL (not null, unique)                  |
| `publish_date`| DATE    | Publication date of the article                 |
| `created_at`  | DATETIME| Timestamp when the article was added to the DB  |

## Logging

All activities (e.g., page fetches, article counts, errors) are logged to `scraper_log.log` with timestamps. Example log entry:

```
2025-05-01 10:15:23.456789 - Fetching kompas.com: Date 2025-05-01, Page 1
2025-05-01 10:15:24.123456 - Found 25 articles.
```

## Notes

- The scraper targets the news index page of Kompas.com (`https://indeks.kompas.com/`).
- It scrapes articles for the current date only. To scrape for different dates, modify the `today` variable in the `scrape_kompas` function.
- The script uses a User-Agent header to mimic a browser request. Adjust the `headers` dictionary in `scrape_kompas` if needed.
- Random delays (`1-3 seconds`) are added between requests to reduce the risk of being blocked by the server.
- Duplicate URLs are handled by the database's `UNIQUE` constraint on the `url` column, skipping insertion of duplicates.
