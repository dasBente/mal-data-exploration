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
    res = requests.get(f"https://api.jikan.moe/v4/anime/{id}/full")
    if res.status_code != 200: break
    
    anime_data = res.json()
    sleep(1)
    
    for tag in ["characters", "staff", "statistics", "moreinfo", "recommendations"]:
        res = requests.get(f"https://api.jikan.moe/v4/anime/{id}/{tag}")
        anime_data[tag] = res.json()["data"] if res.status_code == 200 else []
        sleep(1)
    
    # paginated
    for tag in ["episodes", "reviews", "news"]:
        i = 1
        items = []
        
        while True:
            res = requests.get(f"https://api.jikan.moe/v4/anime/{id}/{tag}?page={i}")
            sleep(1)
            
            if res.status_code != 200:
                anime_data[tag] = items
                break
        
            tag_data = res.json()
            items += tag_data["data"]
            
            if not tag_data["pagination"]["has_next_page"]:
                anime_data[tag] = items
                break
            
    db["anime_raw"].insert_one(anime_data)
    