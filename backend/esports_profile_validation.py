import requests
import re
import os
from dotenv import load_dotenv
import json

class EsportsProfileValidator:
    def __init__(self):
        load_dotenv()
        self.faceit_api_key = os.getenv("FACEIT_API_KEY", "YOUR_FACEIT_API_KEY")
        self.steam_api_key = os.getenv("STEAM_API_KEY", "YOUR_STEAM_API_KEY")

        # Palavras-chave relacionadas a e-sports para validação
        self.esports_keywords = [
            "csgo", "counter-strike", "valorant", "league of legends", "lol",
            "dota", "overwatch", "fortnite", "pubg", "apex legends", "rainbow six"
        ]

        # Plataformas suportadas
        self.supported_platforms = {
            "faceit": self.validate_faceit,
            "steam": self.validate_steam
        }

    def validate_faceit(self, nickname):
        url = f"https://open.faceit.com/data/v4/players?nickname={nickname}"
        headers = {"Authorization": f"Bearer {self.faceit_api_key}"}

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            if 'errors' in data:
                return {"valid": False, "error": data.get('errors', [{}])[0].get('message', 'Unknown error')}

            # Extrair dados relevantes
            profile_data = {
                "valid": True,
                "platform": "faceit",
                "nickname": nickname,
                "profile_url": f"https://www.faceit.com/en/players/{nickname}",
                "player_id": data.get('player_id'),
                "country": data.get('country')
            }

            # Adicionar dados de jogos se disponíveis
            games = data.get('games', {})
            if 'csgo' in games:
                profile_data["csgo"] = {
                    "skill_level": games['csgo'].get('skill_level'),
                    "elo": games['csgo'].get('faceit_elo')
                }
            if 'valorant' in games:
                profile_data["valorant"] = {
                    "skill_level": games['valorant'].get('skill_level'),
                    "elo": games['valorant'].get('faceit_elo')
                }

            return profile_data
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def validate_steam(self, steam_id):
        # Verificar se é um ID numérico ou vanity URL
        if not steam_id.isdigit() and not steam_id.startswith('7656119'):
            # Tentar resolver vanity URL
            resolve_url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={self.steam_api_key}&vanityurl={steam_id}"
            try:
                resolve_response = requests.get(resolve_url)
                resolve_data = resolve_response.json()
                if resolve_data['response']['success'] == 1:
                    steam_id = resolve_data['response']['steamid']
                else:
                    return {"valid": False, "error": "Invalid Steam ID or vanity URL"}
            except Exception as e:
                return {"valid": False, "error": str(e)}

        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.steam_api_key}&steamids={steam_id}"

        try:
            response = requests.get(url)
            data = response.json()

            if not data['response']['players']:
                return {"valid": False, "error": "Steam profile not found"}

            player = data['response']['players'][0]

            # Obter jogos do usuário
            games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.steam_api_key}&steamid={steam_id}&format=json&include_appinfo=1"
            games_response = requests.get(games_url)
            games_data = games_response.json()

            # Filtrar jogos de e-sports populares
            esports_games = []
            if 'games' in games_data.get('response', {}):
                esports_game_ids = {
                    730: "CS:GO",
                    570: "Dota 2",
                    578080: "PUBG",
                    252950: "Rocket League",
                    1172470: "Apex Legends"
                }

                for game in games_data['response']['games']:
                    if game['appid'] in esports_game_ids:
                        esports_games.append({
                            "name": esports_game_ids[game['appid']],
                            "playtime_hours": round(game['playtime_forever'] / 60, 1)
                        })

            return {
                "valid": True,
                "platform": "steam",
                "nickname": player.get('personaname'),
                "profile_url": player.get('profileurl'),
                "avatar": player.get('avatarfull'),
                "status": player.get('personastate'),
                "esports_games": esports_games
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def validate_profile_url(self, url):
        """Valida uma URL de perfil de e-sports e extrai informações relevantes"""
        try:
            # Verificar se a URL é válida
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return {"valid": False, "error": "Invalid profile URL"}

            # Identificar a plataforma com base na URL
            platform = None
            username = None

            if "faceit.com" in url:
                platform = "faceit"
                match = re.search(r'players/([^/]+)', url)
                if match:
                    username = match.group(1)
            elif "steamcommunity.com" in url:
                platform = "steam"
                if "/id/" in url:
                    match = re.search(r'/id/([^/]+)', url)
                    if match:
                        username = match.group(1)
                elif "/profiles/" in url:
                    match = re.search(r'/profiles/([^/]+)', url)
                    if match:
                        username = match.group(1)

            if not platform or not username:
                return {"valid": False, "error": "Unsupported platform or couldn't extract username"}

            # Validar o perfil na plataforma específica
            if platform in self.supported_platforms:
                result = self.supported_platforms[platform](username)
                result["source_url"] = url
                return result
            else:
                return {"valid": False, "error": f"Platform {platform} validation not implemented"}

        except Exception as e:
            return {"valid": False, "error": str(e)}

    def analyze_profile_relevance(self, profile_data, user_interests):
        """
        Analisa a relevância do perfil de e-sports para o usuário
        Versão simplificada sem AWS Comprehend
        """
        try:
            # Preparar texto para análise
            profile_text = json.dumps(profile_data).lower()

            # Calcular pontuação de relevância
            relevance_score = 0
            matching_interests = []

            for interest in user_interests:
                interest_lower = interest.lower()
                # Verificar se o interesse aparece nos dados do perfil
                if interest_lower in profile_text:
                    relevance_score += 1
                    matching_interests.append(interest)

            # Normalizar pontuação (0-100)
            if user_interests:
                normalized_score = min(100, (relevance_score / len(user_interests)) * 100)
            else:
                normalized_score = 0

            # Determinar nível de relevância
            if normalized_score >= 70:
                relevance_level = "high"
            elif normalized_score >= 40:
                relevance_level = "medium"
            else:
                relevance_level = "low"

            return {
                "relevance_score": normalized_score,
                "relevance_level": relevance_level,
                "matching_interests": matching_interests
            }

        except Exception as e:
            return {
                "relevance_score": 0,
                "relevance_level": "unknown",
                "error": str(e)
            }