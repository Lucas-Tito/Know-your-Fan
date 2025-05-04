import requests
import re
import os
import aiohttp
import json
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

class EsportsProfileValidator:
    def __init__(self):
        self.steam_api_key = os.getenv("STEAM_API_KEY") or "YOUR_STEAM_API_KEY"
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

        self.esports_keywords = [
            "csgo", "counter-strike", "overwatch",
            "pubg", "apex legends", "rainbow six", "dota"
        ]

    async def validate_with_ai(self, profile_data: dict, user_interests: List[str]) -> dict:
        """Validates profile relevance using AI analysis"""
        prompt = f"""
        Analyze this esports profile and evaluate its relevance to the user's interests.

        Profile Data:
        - Platform: {profile_data.get('platform')}
        - Nickname: {profile_data.get('nickname')}
        - Games: {', '.join([g['name'] for g in profile_data.get('esports_games', [])])}
        - CS2 Stats: {profile_data.get('cs2_stats', {}).get('basic_stats', {}).get('total_kills', 0)} kills

        User Interests: {', '.join(user_interests)}

        Respond in JSON format with (the response must be in brazilian portuguese):
        {{
            "relevant": boolean,
            "confidence": float (0-1),
            "reason": "detailed explanation",
            "tags": ["list", "of", "tags"]
        }}
        """

        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "anthropic/claude-3-haiku",  # Fast and cost-effective
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.openrouter_url,
                    headers=headers,
                    json=payload,
                    timeout=10
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return json.loads(data["choices"][0]["message"]["content"])
        except Exception as e:
            print(f"AI validation error: {str(e)}")
            return {
                "relevant": False,
                "confidence": 0,
                "reason": "AI validation failed",
                "tags": []
            }

    async def analyze_profile_relevance(self, profile_data: dict, user_interests: List[str]) -> dict:
        """Combines programmatic and AI analysis"""
        # Basic rule-based analysis
        basic_relevance = any(
            game["name"].lower() in [i.lower() for i in user_interests]
            for game in profile_data.get("esports_games", [])
        )

        # AI analysis
        ai_analysis = await self.validate_with_ai(profile_data, user_interests)

        return {
            "basic_relevance": basic_relevance,
            "ai_analysis": ai_analysis,
            "final_relevance": basic_relevance or ai_analysis.get("relevant", False)
        }

    def validate_steam(self, steam_id):
        """Validates a Steam profile and retrieves detailed information"""
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

            # Get CS2 statistics
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
        """Retrieves detailed CS2 statistics"""
        stats_url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?key={self.steam_api_key}&steamid={steam_id}&appid=730"
        stats_response = requests.get(stats_url)
        stats_data = stats_response.json()

        if "playerstats" not in stats_data:
            return None

        stats = {}
        achievements = []

        for stat in stats_data["playerstats"].get("stats", []):
            stats[stat["name"]] = stat["value"]

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
        steam_url_patterns = [
            r'https?://steamcommunity\.com/profiles/(\d+)',
            r'https?://steamcommunity\.com/id/([^/]+)'
        ]

        for pattern in steam_url_patterns:
            match = re.match(pattern, profile_url)
            if match:
                return self.validate_steam(match.group(1))

        return {"valid": False, "error": "Invalid Steam profile URL"}