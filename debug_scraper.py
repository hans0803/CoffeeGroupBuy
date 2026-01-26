
import requests
from bs4 import BeautifulSoup

url = "https://www.oklaocoffee.net/pages/oklao-new-year-coffee-gift-box"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    
    print(f"Page Title: {soup.title.string}")
    
    # Try current selector
    items = soup.select('a.Product-item')
    print(f"Original Selector (a.Product-item) found: {len(items)}")
    
    if len(items) > 0:
        first = items[0]
        print("\n--- First Item HTML ---")
        # print(first.prettify()[:500])
        
        img = first.select_one('img')
        if img:
            print("\n--- Image Tag ---")
            print(img)
            print(f"src: {img.get('src')}")
            print(f"data-src: {img.get('data-src')}")
        else:
            print("\nNo img tag found in first item")
            
except Exception as e:
    print(f"Error: {e}")
