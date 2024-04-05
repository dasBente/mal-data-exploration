import os
from time import sleep
from pymongo import MongoClient
import requests

MONGODB_URL = os.environ.get("MONGODB_URL")
if MONGODB_URL == None: raise Exception("No database URL given, please specify `MONGODB_URL`")

MONGODB_NAME = os.environ.get("MONGODB_NAME")
if MONGODB_NAME == None: raise Exception("No database name given, please specify `MONGODB_NAME`")

# connection
db = MongoClient(MONGODB_URL)[MONGODB_NAME]

# scrape all anime
id = 1
success = True

while True:
    res = requests.get(f"http://api.jikan.moe/v4/anime/{id}/full")
    if res.status_code != 200: break
    
    anime_data = res.json()["data"]
    print(f"Downloading {anime_data['title']} with ID {id}")
    sleep(1)
    
    for tag in ["characters", "staff", "statistics", "moreinfo", "recommendations"]:
        print(f"Downloading {tag}")
        res = requests.get(f"http://api.jikan.moe/v4/anime/{id}/{tag}")
        anime_data[tag] = res.json()["data"] if res.status_code == 200 else []
        sleep(1)
    
    # paginated
    for tag in ["episodes", "reviews", "news"]:
        i = 1
        items = []
        
        while True:
            print(f"Downloading {tag}, page {i}")
            
            res = requests.get(f"http://api.jikan.moe/v4/anime/{id}/{tag}?page={i}")
            tag_data = res.json()            
            sleep(1)
            
            if res.status_code != 200 or not "data" in tag_data or len(tag_data["data"]) == 0:
                anime_data[tag] = items
                print(f"[{tag}] Stopped with {res.status_code} for {str(tag_data)} on page {i}")
                break
            
            items += tag_data["data"]
            i += 1
    
    db["anime_raw"].update_one({"mal_id": id}, {"$set": anime_data}, True)
    id += 1
    