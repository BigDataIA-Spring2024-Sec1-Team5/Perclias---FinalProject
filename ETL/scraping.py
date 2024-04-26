from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
from concurrent.futures import ThreadPoolExecutor

def setup_driver():
   options = webdriver.ChromeOptions()
   options.add_argument('headless')
   driver = webdriver.Chrome(options=options)
   return driver

def scrape_content(link):
   driver = setup_driver()
   driver.get(link)
   time.sleep(3)
   page_soup = BeautifulSoup(driver.page_source, 'html.parser')
   driver.quit()
   heading = page_soup.find('h1')
   heading_text = heading.text.strip() if heading else "No heading found"
   content = page_soup.find('div', id='d-article').text.strip()
   cleaned_content = content.replace('Expand Section', '')
   cleaned_content = cleaned_content.replace('To use the sharing features on this page, please enable JavaScript.', '')
   return (heading_text, cleaned_content)

def get_all_links():
   driver = setup_driver()
   all_links = []
   for letter in range(ord('A'), ord('Z') + 1):
       url = f"https://medlineplus.gov/ency/encyclopedia_{chr(letter)}.htm"
       driver.get(url)
       soup = BeautifulSoup(driver.page_source, 'html.parser')
       links = [f"https://medlineplus.gov/ency/{li['href']}" for li in soup.select('#index li a')]
       all_links.extend(links)
   driver.quit()
   return all_links

def scraping_task():
   links = get_all_links()
   results = []
   with ThreadPoolExecutor(max_workers=12) as executor:
       results = list(executor.map(scrape_content, links))
   with open('/Users/shubh/anaconda3/lib/python3.10/site-packages/airflow/example_dags/Airflow DAG/Medline.csv', 'w', newline='', encoding='utf-8') as file:
       writer = csv.writer(file)
       writer.writerow(['Title', 'Content'])
       for title, content in results:
           writer.writerow([title, content])