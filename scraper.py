import requests
from bs4 import BeautifulSoup
import json
import random
import time

def get_html(url):
    # Kasutame erinevaid "User-Agent" päiseid, et mitte vahele jääda
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ]
    headers = {'User-Agent': random.choice(user_agents)}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.content
    except:
        return None

def korja_uudised():
    uudised = []
    
    # 1. ERR (Väga lihtne struktuur)
    print("Kogun ERR...")
    content = get_html("https://www.err.ee/")
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.select('header h2 a, header h1 a')[:5]:
            uudised.append({
                "allikas": "ERR",
                "pealkiri": link.get_text(strip=True),
                "link": link['href']
            })

    # 2. Delfi
    print("Kogun Delfi...")
    content = get_html("https://www.delfi.ee/")
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.select('h1 a, h3 a')[:5]:
            title = link.get_text(strip=True)
            if len(title) > 20: # Ainult pikemad pealkirjad
                uudised.append({
                    "allikas": "Delfi",
                    "pealkiri": title,
                    "link": link['href']
                })

    return uudised

if __name__ == "__main__":
    andmed = korja_uudised()
    
    # Kui ikka midagi ei leidnud, paneme test-uudise, et näha kas torud töötavad
    if not andmed:
        andmed = [{"allikas": "Test", "pealkiri": "Süsteem töötab, aga uudiseid ei leitud.", "link": "#"}]
    
    with open('uudised.json', 'w', encoding='utf-8') as f:
        json.dump(andmed, f, ensure_ascii=False, indent=4)
    print(f"Kokku saime {len(andmed)} kirjet.")
