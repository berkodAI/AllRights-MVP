import requests
from bs4 import BeautifulSoup

api_urls = {
    "default_search": {
        "url": "https://influencersgonewild.com/wp-admin/admin-ajax.php?action=bimber_search&bimber_term={}",
        "method": "GET",
        "params": {},
        "headers": {},
        "parse": {
            "results": {
                "selector": "li",
                "attributes": {
                    "title": {
                        "selector": "h3.entry-title a",
                        "attribute": "text"
                    },
                    "link": {
                        "selector": "h3.entry-title a",
                        "attribute": "href"
                    },
                    "thumbnail": {
                        "selector": "div.entry-featured-media img",
                        "attribute": "src"
                    },
                    "upload_date": {
                        "selector": "time.entry-date",
                        "attribute": "datetime"
                    }
                }
            }
        }
    }
}

def fetch_search_results(term):
    search_url = api_urls["default_search"]["url"].format(term)
    response = requests.get(search_url)
    
    if response.status_code == 200:
        results = []
        data = response.json()
        html_content = data.get("html", "")
        
        soup = BeautifulSoup(html_content, "html.parser")
        items = soup.select(api_urls["default_search"]["parse"]["results"]["selector"])
        
        for item in items:
            title_selector = api_urls["default_search"]["parse"]["results"]["attributes"]["title"]["selector"]
            link_selector = api_urls["default_search"]["parse"]["results"]["attributes"]["link"]["selector"]
            thumbnail_selector = api_urls["default_search"]["parse"]["results"]["attributes"]["thumbnail"]["selector"]
            date_selector = api_urls["default_search"]["parse"]["results"]["attributes"]["upload_date"]["selector"]
            
            title = item.select_one(title_selector).get_text(strip=True)
            link = item.select_one(link_selector)["href"]
            thumbnail = item.select_one(thumbnail_selector)["src"]
            upload_date = item.select_one(date_selector)["datetime"] if item.select_one(date_selector) else None
            
            results.append({
                "title": title,
                "link": link,
                "thumbnail": thumbnail,
                "upload_date": upload_date
            })
        
        return results
    else:
        return []

def scrape_and_return_image_urls(search_query):
    results = fetch_search_results(search_query)
    return results
