import requests
from bs4 import BeautifulSoup

class EsportsProfileValidator:
    def __init__(self):
        self.faceit_api_key = "YOUR_FACEIT_API_KEY"
        self.steam_api_key = "YOUR_STEAM_API_KEY"

    def validate_faceit(self, nickname):
        url = f"https://api.faceit.com/core/v1/users?nickname={nickname}"
        headers = {"Authorization": f"Bearer {self.faceit_api_key}"}

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            return {
                "valid": True,
                "level": data['games']['csgo']['skill_level'],
                "elo": data['games']['csgo']['faceit_elo'],
                "matches": data['games']['csgo']['matches']
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_steam(self, steam_id):
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.steam_api_key}&steamids={steam_id}"

        try:
            response = requests.get(url)
            data = response.json()

            return {
                "valid": True,
                "profile": data['response']['players'][0]
            }
        except Exception as e:
            return {"error": str(e)}