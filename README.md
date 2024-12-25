# Web Scraper for Product Data

This project is a Python-based web scraper that collects product data from a website. It uses **Selenium** for browser automation, **Cloudscraper** for bypassing anti-bot protection, and **BeautifulSoup** for parsing HTML.

## Features

- Retrieves product information (name, description, image link, product link) from a website.
- Stores cookies in a JSON file to bypass login/anti-bot checks.
- Uses headless Chrome to fetch cookies when necessary.
- Saves scraped product data into a `products.json` file.
- Avoids scraping duplicate products by checking against previously saved data.

## Requirements

Before running the scraper, ensure that you have the following installed:

- Python 3.6 or later
- Chrome browser installed
- `chromedriver` (handled by `webdriver_manager`)
- Python packages:
  - `selenium`
  - `cloudscraper`
  - `beautifulsoup4`
  - `webdriver_manager`

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

# Usage
1. Clone the repository or download the script files.
2. Update the url variable in the script with the URL of the website you want to scrape.
3. Run the script:
```bash
py scraper.py
```


