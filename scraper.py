import json
import os
import cloudscraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


COOKIE_FILE = "cookies.json" # File to store cookies
url = 'URL HERE' # URL of the website to scrape

def get_browser_cookies(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    driver.implicitly_wait(5)

    cookies = driver.get_cookies()
    driver.quit()

    with open(COOKIE_FILE, "w") as file:
        json.dump(cookies, file)
    
    return cookies

def load_cookies():
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r") as file:
            return json.load(file)
    return None

def get_cloudscraper_response(url, cookies):
    scraper = cloudscraper.create_scraper()

    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    
    response = scraper.get(url, cookies=cookies_dict)
    return response

def main():
    cookies = load_cookies()
    if os.path.exists('products.json'):
        os.remove('products.json')

    if not cookies:
        print("Cookies not found, fetching with Selenium...")
        cookies = get_browser_cookies(url)

    response = get_cloudscraper_response(url, cookies)

    if response.status_code == 503:
        print("Cookies have expired, fetching with Selenium...")
        cookies = get_browser_cookies(url)
        return


    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            if "product/" in link.get('href'):
                response = get_cloudscraper_response(link.get('href'), cookies)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    name = soup.find('div', {'x-data': 'productForm'}).find('h1').text
                    description = soup.find('p', {'class': 'e-paragraph'}).text
                    image_link = soup.find('img').get('src')

                    data = [
                        {
                            'name': name,
                            'description': description,
                            'image_link': image_link,
                            'product_link': link.get('href')
                        } 
                    ]

                    if os.path.exists('products.json'):
                        with open('products.json', 'r') as file:
                            try:
                                json_data = json.load(file)
                            except json.JSONDecodeError:
                                json_data = []

                        if any(item['name'] == data[0]['name'] for item in json_data):
                            print(f"Product '{data[0]['name']}' already exists. Skipping.")
                        else:
                            json_data.extend(data)
                            with open('products.json', 'w') as file:
                                json.dump(json_data, file, indent=4)
                    else:
                        with open('products.json', 'w') as file:
                            json.dump(data, file, indent=4)


                else:
                    print(f"Request failed with status code: {response.status_code}")


        with open('products.json', 'r') as file:
            json_data = json.load(file)
            print(f"Scraped {len(json_data)} products successfully to products.json.")

    else:
        print(f"Request failed with status code: {response.status_code}")
    pass

if __name__ == "__main__":
    main()
