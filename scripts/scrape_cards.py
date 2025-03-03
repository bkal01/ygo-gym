import json
import requests

YGORESOURCES_API_URL = "https://db.ygoresources.com/data/"

def scrape_card_ids():
    url = f"{YGORESOURCES_API_URL}idx/card/name/en"
    try:
        response = requests.get(url)
        response.raise_for_status()
        card_name_to_id = response.json()
        
        try:
            with open("data/card_names.txt", "r") as f:
                card_names = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Error: data/card_names.txt not found")
            return
        
        results = []
        for name in card_names:
            if name in card_name_to_id:
                card_id = card_name_to_id[name]
                results.append(card_id[0])
        
        with open("data/card_ids.txt", "w") as f:
            for card_id in results:
                f.write(f"{card_id}\n")
        
        print(f"Found {len(results)} card IDs out of {len(card_names)} card names")
        
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
