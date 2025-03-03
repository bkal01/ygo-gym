import json
import requests
import time

from tqdm import tqdm

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

def scrape_card_infos():
    try:
        with open("data/card_ids.txt", "r") as f:
            card_ids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: data/card_ids.txt not found")
        return
    
    card_infos = []
    total_cards = len(card_ids)
    
    for card_id in tqdm(card_ids, total=total_cards):
        url = f"{YGORESOURCES_API_URL}card/{card_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            card_info = response.json()
            card_infos.append(card_info)
        except requests.RequestException as e:
            print(f"Error fetching data for card ID {card_id}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for card ID {card_id}: {e}")
        
        time.sleep(1)
    
    with open("data/card_infos.json", "w") as f:
        json.dump(card_infos, f, indent=2)
    
    print(f"Successfully fetched {len(card_infos)} out of {total_cards} cards")