import time
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 
    

global_count=0

def scrape_website(url):
    driver.get(url)
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(10): 
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def download_images(soup, query):
    global global_count
    images = soup.find_all('img')
    if not os.path.exists(query):
        os.makedirs(query)
    for image in images:
        image_url = image.get('src')
        try:
            print(image_url)
            print(str(image_url).split(".")[-1])
            img=requests.get(image_url,headers=headers).content
            if len(img)>50000:
                f = open(f'{query}/image{str(global_count) +"."+ str(image_url).split(".")[-1]}','wb')
                f.write(img)
                f.close()
                print(f"Downloaded image {global_count}")
                global_count+=1
        except Exception as e:
            print(f"Failed to download image {global_count}")
            print(repr(e))
    

def main():
    search_query = input("Enter search query (default: Taylor Swift): ") or "Taylor Swift"
    urls = [
        "https://influencersgonewild.com/?s=" + search_query.lower().replace(' ', '+'),
        "https://leakedzone.com/search?search=" + search_query.lower().replace(' ', '+'),
        "https://mrdeepfakes.com/photos/celebrities/"+ search_query.lower().replace(' ', '-'), 
        "https://deepfake-xxx.com/",
        "https://deepfakesporn.com/search/video/?s=" + search_query.lower().replace(' ', '+'),
        "https://celebdeepfakes.net/?s=" + search_query.lower().replace(' ', '+'),
        "https://deepfake-porn.com/?s=" + search_query.lower().replace(' ', '+'),
    ]

    for url in urls:
        print(f"Scraping {url}")
        print(f'[href*="{search_query.lower().replace(" ", "-")}"]')
        internURLS = [link['href'] for link in scrape_website(url).select(f'[href*="{search_query.lower().replace(" ", "-")}"]')] 
        for internURL in internURLS:
            print(internURL)
            url=urlparse(url)
            parsedURL=urlparse(internURL)
            #if split
            if parsedURL.scheme not in ["http", "https"]: 
                internURL=url.scheme + "://" + url.netloc+"/"+ url
            soup = scrape_website(internURL)
            download_images(soup, search_query)

if __name__ == "__main__":
    main()
    driver.quit()
