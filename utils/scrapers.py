import requests

def anime_parser(id, collection):
    data = requests.get(f"https://api.jikan.moe/v4/anime/{id}/full").json()