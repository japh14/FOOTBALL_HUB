import requests
import os

from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
API_KEY = os.getenv("API_KEY")

base_url = "https://v3.football.api-sports.io/"
full_url = f"{base_url}status"

headers = {
    "x-apisports-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

response = requests.get(full_url, headers=headers)
data = response.json()
pprint(data)