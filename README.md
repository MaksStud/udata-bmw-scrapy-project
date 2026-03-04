## 1.Clone

```
# Setup and Launch Guide

## 1. Environment Setup
[cite_start]Ensure you are using **Python 3.10+**[cite: 12].

```bash
# Clone the repository
git clone <your-repository-url>
cd bmw_scraper

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

## 2. Installation

Install the **Scrapy** framework and **Playwright** for browser automation.

**Bash**

```
pip install -r requirements.txt
playwright install chromium
```

## 3. Running the Scraper

By default, the spider scrapes the first **5 pages** as required.

**Bash**

```
# Standard run
scrapy crawl bmw_uk

```

## 4. Viewing Results

The data is stored in a **SQLite** database file named `bmw_cars.db`.

**Bash**

```
# Open database via terminal
sqlite3 bmw_cars.db

# Quick query to check data
SELECT * FROM cars LIMIT 5;
```

## 5. Requirements Check

* **Database:**`bmw_cars.db`.
* **Table:**`cars` with `registration` as the primary key.
* **Logging:** User-Agent rotation logs are visible at the `DEBUG` level.
