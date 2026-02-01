import requests
from bs4 import BeautifulSoup
import json

def get_rss_news(feed_url, source_name):
    uudised = []
    # Maskeering, et Delfi meid sisse laseks
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    
    try:
        print(f"Loen: {source_name} ({feed_url})...")
        response = requests.get(feed_url, headers=headers, timeout=10)
        
        # 'xml' parser on RSS jaoks parim
        soup = BeautifulSoup(response.content, 'xml')
        
        # Võtame igast kanalist max 5 värskemat uudist
        items = soup.find_all('item', limit=5)
        
        for item in items:
            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)
            
            # Puhastame linke
            if link:
                uudised.append({
                    "allikas": source_name, # Kõik lähevad "Delfi" nime alla
                    "pealkiri": title,
                    "link": link
                })
    except Exception as e:
        print(f"Viga {source_name}-ga: {e}")

    return uudised

if __name__ == "__main__":
    koik_uudised = []
    
    # SIIN ON UUS ALLIKATE NIMEKIRI
    rss_allikad = [
        # ERR
        ("https://www.err.ee/rss", "ERR"),
        
        # Postimees
        ("https://rss.postimees.ee/?section=81", "Postimees"), 
        
        # Eestinen
        ("https://eestinen.fi/feed/", "Eestinen"),
        
        # --- DELFI PAKETT ---
        ("https://feeds.delfi.ee/rss/delfi/uudised", "Delfi"),  # Peauudised
        ("https://feeds.delfi.ee/rss/delfi/majandus", "Delfi"), # Ärileht
        ("https://feeds.delfi.ee/rss/delfi/sport", "Delfi"),    # Sport
        ("https://feeds.delfi.ee/rss/delfi/forte", "Delfi")     # Teadus
    ]
    
    for url, nimi in rss_allikad:
        koik_uudised.extend(get_rss_news(url, nimi))
    
    # Turvavõrk, et fail kunagi tühi ei oleks
    if not koik_uudised:
        koik_uudised.append({"allikas": "Süsteem", "pealkiri": "Hetkel uudiseid ei saadud kätte.", "link": "#"})

    with open('uudised.json', 'w', encoding='utf-8') as f:
        json.dump(koik_uudised, f, ensure_ascii=False, indent=4)
    
    print(f"Valmis! Salvestasin kokku {len(koik_uudised)} uudist.")
