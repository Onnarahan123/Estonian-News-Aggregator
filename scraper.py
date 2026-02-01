import requests
from bs4 import BeautifulSoup
import json

def get_news(url, source_name, selector, class_name):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        for item in soup.find_all(selector, class_=class_name, limit=5):
            title = item.get_text(strip=True)
            link_tag = item.find('a') if item.name != 'a' else item
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else url
            
            if not link.startswith('http'):
                link = url.rstrip('/') + link
                
            news_items.append({"allikas": source_name, "pealkiri": title, "link": link})
        return news_items
    except Exception as e:
        print(f"Viga {source_name} kraapimisel: {e}")
        return []

if __name__ == "__main__":
    sources = [
        ("https://www.err.ee/", "ERR", "header", ""),
        ("https://www.postimees.ee/", "Postimees", "h1", "article-headline"),
        ("https://eestinen.fi/", "Eestinen", "h3", "entry-title"),
        ("https://www.delfi.ee/", "Delfi", "h1", "C-headline__title")
    ]
    
    koik_uudised = []
    for url, name, sel, cls in sources:
        print(f"Kogun: {name}...")
        koik_uudised.extend(get_news(url, name, sel, cls))
    
    with open('uudised.json', 'w', encoding='utf-8') as f:
        json.dump(koik_uudised, f, ensure_ascii=False, indent=4)
    print("Uudised salvestatud!")
