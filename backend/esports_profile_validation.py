import requests
import re
import os
from dotenv import load_dotenv

class EsportsProfileValidator:
    def __init__(self):
        load_dotenv()
        self.steam_api_key = os.getenv("STEAM_API_KEY") or "YOUR_STEAM_API_KEY"

        # E-sports related keywords for validation
        self.esports_keywords = [
            "csgo", "counter-strike", "valorant", "overwatch", "fortnite", "pubg", "apex legends", "rainbow six"
        ]

    def validate_steam(self, steam_id):
        """
        Validates a Steam profile and retrieves detailed information including CS2 statistics.
        """
        try:
            # Check if it's a numeric ID or vanity URL
            if not steam_id.isdigit() and not steam_id.startswith('7656119'):
                # Resolve vanity URL
                resolve_url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={self.steam_api_key}&vanityurl={steam_id}"
                resolve_response = requests.get(resolve_url)
                resolve_data = resolve_response.json()
                if resolve_data['response']['success'] == 1:
                    steam_id = resolve_data['response']['steamid']
                else:
                    return {"valid": False, "error": "Invalid Steam ID or vanity URL"}

            # Get basic profile information
            profile_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.steam_api_key}&steamids={steam_id}"
            profile_response = requests.get(profile_url)
            profile_data = profile_response.json()

            if not profile_data['response']['players']:
                return {"valid": False, "error": "Steam profile not found"}

            player = profile_data['response']['players'][0]

            # Get CS2 statistics (appid 730)
            cs2_stats = self._get_cs2_stats(steam_id)
            if not cs2_stats:
                return {"valid": False, "error": "CS2 stats not found"}

            # Get owned e-sports games
            esports_games = self._get_esports_games(steam_id)

            return {
                "valid": True,
                "platform": "steam",
                "nickname": player.get('personaname'),
                "profile_url": player.get('profileurl'),
                "avatar": player.get('avatarfull'),
                "status": player.get('personastate'),
                "cs2_stats": cs2_stats,
                "esports_games": esports_games
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def _get_cs2_stats(self, steam_id):
        """Retrieves detailed CS2 statistics for a Steam profile"""
        stats_url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?key={self.steam_api_key}&steamid={steam_id}&appid=730"
        stats_response = requests.get(stats_url)
        stats_data = stats_response.json()

        if "playerstats" not in stats_data:
            return None

        # Process CS2 stats into a more usable format
        stats = {}
        achievements = []

        # Basic stats
        for stat in stats_data["playerstats"].get("stats", []):
            stats[stat["name"]] = stat["value"]

        # Achievements
        for achievement in stats_data["playerstats"].get("achievements", []):
            achievements.append({
                "name": achievement["name"],
                "achieved": bool(achievement["achieved"])
            })

        return {
            "basic_stats": stats,
            "achievements": achievements,
            "steam_id": stats_data["playerstats"].get("steamID"),
            "game_name": stats_data["playerstats"].get("gameName")
        }

    def _get_esports_games(self, steam_id):
        """Retrieves list of owned e-sports games"""
        owned_games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={self.steam_api_key}&steamid={steam_id}&include_appinfo=true"
        owned_games_response = requests.get(owned_games_url)
        owned_games_data = owned_games_response.json()

        esports_games = []
        if "response" in owned_games_data and "games" in owned_games_data["response"]:
            for game in owned_games_data["response"]["games"]:
                if any(keyword in game["name"].lower() for keyword in self.esports_keywords):
                    esports_games.append({
                        "name": game["name"],
                        "appid": game["appid"],
                        "playtime_hours": round(game["playtime_forever"] / 60, 1),
                        "img_icon_url": f"http://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_icon_url']}.jpg"
                    })

        return esports_games

    def validate_profile_url(self, profile_url):
        """
        Validates a Steam profile URL and extracts the Steam ID
        """
        # Steam profile URL patterns
        steam_url_patterns = [
            r'https?://steamcommunity\.com/profiles/(\d+)',
            r'https?://steamcommunity\.com/id/([^/]+)'
        ]

        for pattern in steam_url_patterns:
            match = re.match(pattern, profile_url)
            if match:
                return self.validate_steam(match.group(1))

        return {"valid": False, "error": "Invalid Steam profile URL"}