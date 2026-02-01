import requests
from bs4 import BeautifulSoup
import json

def get_err_news():
    url = "https://www.err.ee/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_items = []
    
    # ERR pealkirjad on tavaliselt 'header' või 'a' sees teatud klassiga
    for article in soup.find_all('header', limit=5):
        title = article.get_text(strip=True)
        link = article.find('a')['href'] if article.find('a') else url
        news_items.append({"allikas": "ERR", "pealkiri": title, "link": link})
    
    return news_items

def get_delfi_news():
    url = "https://www.delfi.ee/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_items = []
    
    # Delfi kasutab tihti klasse nagu 'C-headline__title'
    for title_tag in soup.find_all('h1', class_='C-headline__title', limit=5):
        title = title_tag.get_text(strip=True)
        link = title_tag.find_parent('a')['href'] if title_tag.find_parent('a') else url
        news_items.append({"allikas": "Delfi", "pealkiri": title, "link": link})
        
    return news_items

def salva_uudised(andmed):
    with open('uudised.json', 'w', encoding='utf-8') as f:
        json.dump(andmed, f, ensure_ascii=False, indent=4)
    print(f"Salvestatud {len(andmed)} uudist faili uudised.json")

if __name__ == "__main__":
    koik_uudised = get_err_news() + get_delfi_news()
    salva_uudised(koik_uudised)
