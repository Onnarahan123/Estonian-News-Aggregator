import requests
from bs4 import BeautifulSoup
import json

def get_rss_news(feed_url, source_name):
    uudised = []
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; UudisteBot/1.0)'}
    
    try:
        print(f"Loen RSS voogu: {source_name}...")
        response = requests.get(feed_url, headers=headers, timeout=10)
        # Kasutame 'xml' parserit, sest RSS on XML formaadis
        soup = BeautifulSoup(response.content, 'xml')
        
        # RSS-is on uudised <item> siltide vahel
        items = soup.find_all('item', limit=5)
        
        for item in items:
            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)
            
            # Puhastame linke (mõnikord on seal tühikuid)
            if link:
                uudised.append({
                    "allikas": source_name,
                    "pealkiri": title,
                    "link": link
                })
    except Exception as e:
        print(f"Viga {source_name}-ga: {e}")

    return uudised

if __name__ == "__main__":
    koik_uudised = []
    
    # Need on ametlikud RSS vood
    rss_allikad = [
        ("https://www.err.ee/rss", "ERR"),
        ("https://rss.postimees.ee/?section=81", "Postimees"), 
        ("https://feeds.delfi.ee/rss/delfi/uudised", "Delfi"),
        ("https://eestinen.fi/feed/", "Eestinen")
    ]
    
    for url, nimi in rss_allikad:
        koik_uudised.extend(get_rss_news(url, nimi))
    
    # Kui ikka on tühi (väga ebatõenäoline), siis paneme testi
    if not koik_uudised:
        koik_uudised.append({"allikas": "Süsteem", "pealkiri": "Viga: Ühtegi RSS voogu ei leitud.", "link": "#"})

    with open('uudised.json', 'w', encoding='utf-8') as f:
        json.dump(koik_uudised, f, ensure_ascii=False, indent=4)
    
    print(f"Valmis! Salvestasin {len(koik_uudised)} uudist.")
