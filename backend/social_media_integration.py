import requests
import os
from dotenv import load_dotenv
import json
import re
from bs4 import BeautifulSoup

# Carregar variáveis do arquivo .env
load_dotenv()

class SocialMediaIntegration:
    def __init__(self):
        # Organizações de e-sports para monitorar
        self.esports_orgs = [
            "furia", "furiagaming", "furiagg", "mibr", "pain", "loud",
            "fluxo", "intz", "keyd", "kabum", "rensga"
        ]

        # BlueSky API setup
        self.bluesky_server = os.getenv("BLUESKY_SERVER", "https://bsky.social")

    def link_social_account(self, user_id, platform, username, credentials=None):
        """
        Vincula uma conta de rede social ao perfil do usuário

        Args:
            user_id: ID do usuário no sistema
            platform: Plataforma (twitch, facebook, bluesky)
            username: Nome de usuário na plataforma
            credentials: Credenciais para plataformas que exigem (como BlueSky)

        Returns:
            dict: Status da vinculação e dados básicos do perfil
        """
        try:
            if platform == "twitch":
                profile_data = self.get_twitch_public_data(username)
            elif platform == "facebook":
                profile_data = self.get_facebook_public_data(username)
            elif platform == "bluesky":
                if not credentials or 'identifier' not in credentials or 'password' not in credentials:
                    return {"status": "error", "message": "Credenciais necessárias para BlueSky"}
                auth_result = self.bluesky_login(credentials['identifier'], credentials['password'])
                if auth_result["status"] == "error":
                    return auth_result
                profile_data = self.get_bluesky_data(auth_result["access_jwt"], auth_result["user_info"]["did"])
                profile_data["access_jwt"] = auth_result["access_jwt"]
                profile_data["refresh_jwt"] = auth_result["refresh_jwt"]
                profile_data["did"] = auth_result["user_info"]["did"]
            else:
                return {"status": "error", "message": "Plataforma não suportada"}

            if "error" in profile_data:
                return {"status": "error", "message": profile_data["error"]}

            # Aqui você salvaria a vinculação no banco de dados
            # Por exemplo: database.update_user_social_media(user_id, platform, username, profile_data)

            return {
                "status": "success",
                "message": f"Conta {platform} vinculada com sucesso",
                "profile_data": profile_data
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_twitch_public_data(self, username):
        """
        Obtém dados públicos de um usuário do Twitch
        """
        try:
            # Usar a API pública do Twitch (requer Client-ID mas não OAuth)
            headers = {
                "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
                "Accept": "application/vnd.twitchtv.v5+json"
            }

            # Obter ID do usuário
            user_url = f"https://api.twitch.tv/helix/users?login={username}"
            response = requests.get(user_url, headers=headers)
            user_data = response.json()

            if not user_data.get('data') or len(user_data['data']) == 0:
                return {"error": "Usuário não encontrado"}

            user_info = user_data['data'][0]
            user_id = user_info['id']

            # Obter informações do canal
            channel_url = f"https://api.twitch.tv/helix/channels?broadcaster_id={user_id}"
            channel_response = requests.get(channel_url, headers=headers)
            channel_data = channel_response.json()

            # Obter streams seguidos (não é possível sem OAuth, então usamos dados públicos)
            # Aqui poderíamos usar web scraping como alternativa, mas isso tem limitações

            return {
                "id": user_id,
                "username": username,
                "display_name": user_info.get('display_name'),
                "profile_image": user_info.get('profile_image_url'),
                "description": user_info.get('description'),
                "view_count": user_info.get('view_count'),
                "broadcaster_type": user_info.get('broadcaster_type'),
                "channel_info": channel_data.get('data', [{}])[0] if channel_data.get('data') else {}
            }
        except Exception as e:
            return {"error": str(e)}

    def get_facebook_public_data(self, username):
        """
        Obtém dados públicos de uma página do Facebook
        Nota: Isso é limitado a páginas públicas, não perfis pessoais
        """
        try:
            # Para páginas públicas, podemos usar a API Graph sem token de usuário
            # Mas precisamos de um token de acesso do aplicativo
            app_token_url = f"https://graph.facebook.com/oauth/access_token?client_id={os.getenv('FACEBOOK_APP_ID')}&client_secret={os.getenv('FACEBOOK_APP_SECRET')}&grant_type=client_credentials"
            token_response = requests.get(app_token_url)
            token_data = token_response.json()

            if 'error' in token_data:
                return {"error": token_data['error']['message']}

            app_token = token_data['access_token']

            # Obter dados da página
            page_url = f"https://graph.facebook.com/v18.0/{username}?fields=id,name,category,fan_count,link&access_token={app_token}"
            page_response = requests.get(page_url)
            page_data = page_response.json()

            if 'error' in page_data:
                return {"error": page_data['error']['message']}

            # Verificar se é uma página de e-sports
            is_esports = False
            if any(org in page_data.get('name', '').lower() for org in self.esports_orgs):
                is_esports = True

            return {
                "id": page_data.get('id'),
                "name": page_data.get('name'),
                "category": page_data.get('category'),
                "fan_count": page_data.get('fan_count'),
                "link": page_data.get('link'),
                "is_esports_related": is_esports
            }
        except Exception as e:
            return {"error": str(e)}

    def bluesky_login(self, identifier, password):
        """
        Autentica no BlueSky usando credenciais
        """
        try:
            # Endpoint de autenticação
            auth_url = f"{self.bluesky_server}/xrpc/com.atproto.server.createSession"

            # Dados de autenticação
            auth_data = {
                "identifier": identifier,  # email ou handle
                "password": password
            }

            # Fazer requisição de autenticação
            response = requests.post(auth_url, json=auth_data)
            session_data = response.json()

            if 'error' in session_data:
                return {"status": "error", "message": session_data.get('error', 'Erro de autenticação')}

            return {
                "status": "success",
                "access_jwt": session_data.get('accessJwt'),
                "refresh_jwt": session_data.get('refreshJwt'),
                "user_info": {
                    "did": session_data.get('did'),
                    "handle": session_data.get('handle')
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_bluesky_data(self, access_jwt, did):
        """
        Obtém dados do usuário no BlueSky usando o token JWT
        """
        try:
            # Obter perfil do usuário
            profile_url = f"{self.bluesky_server}/xrpc/app.bsky.actor.getProfile"
            headers = {"Authorization": f"Bearer {access_jwt}"}
            params = {"actor": did}

            profile_response = requests.get(profile_url, headers=headers, params=params)
            profile_data = profile_response.json()

            # Obter timeline do usuário
            timeline_url = f"{self.bluesky_server}/xrpc/app.bsky.feed.getTimeline"
            timeline_response = requests.get(timeline_url, headers=headers, params={"limit": 50})
            timeline_data = timeline_response.json()

            # Analisar posts relacionados a esports
            esports_posts = []
            for feed_item in timeline_data.get('feed', []):
                post = feed_item.get('post', {})
                record = post.get('record', {})
                text = record.get('text', '').lower()

                if any(org in text for org in self.esports_orgs):
                    esports_posts.append({
                        "uri": post.get('uri'),
                        "text": record.get('text', '')[:100],
                        "likes": post.get('likeCount', 0),
                        "reposts": post.get('repostCount', 0)
                    })

            # Obter seguidores
            follows_url = f"{self.bluesky_server}/xrpc/app.bsky.graph.getFollows"
            follows_response = requests.get(follows_url, headers=headers, params={"actor": did})
            follows_data = follows_response.json()

            return {
                "handle": profile_data.get('handle'),
                "display_name": profile_data.get('displayName'),
                "followers_count": profile_data.get('followersCount', 0),
                "following_count": profile_data.get('followsCount', 0),
                "esports_posts": {
                    "count": len(esports_posts),
                    "sample": esports_posts[:5]
                }
            }
        except Exception as e:
            return {"error": str(e)}

    def get_user_esports_activity(self, user_id, linked_accounts):
        """
        Obtém um resumo consolidado das atividades relacionadas a esports
        de todas as contas vinculadas do usuário
        """
        activity_summary = {
            "following_orgs": [],
            "interactions": {
                "total": 0,
                "by_platform": {}
            },
            "favorite_orgs": {},
            "engagement_level": "low"  # low, medium, high
        }

        for account in linked_accounts:
            platform = account["platform"]
            username = account.get("username")

            if platform == "twitch":
                # Para Twitch, usamos dados públicos limitados
                if account.get("is_esports_related", False):
                    activity_summary["following_orgs"].append({
                        "name": account.get("display_name", username),
                        "platform": "twitch"
                    })

                    # Incrementar contagem de interações
                    activity_summary["interactions"]["total"] += 1
                    activity_summary["interactions"]["by_platform"]["twitch"] = activity_summary["interactions"]["by_platform"].get("twitch", 0) + 1

            elif platform == "facebook":
                # Para Facebook, usamos dados de páginas públicas
                if account.get("is_esports_related", False):
                    activity_summary["following_orgs"].append({
                        "name": account.get("name", username),
                        "platform": "facebook",
                        "category": account.get("category")
                    })

                    # Incrementar contagem de interações
                    activity_summary["interactions"]["total"] += 1
                    activity_summary["interactions"]["by_platform"]["facebook"] = activity_summary["interactions"]["by_platform"].get("facebook", 0) + 1

                    # Analisar organizações favoritas
                    for org in self.esports_orgs:
                        if org in account.get("name", "").lower():
                            activity_summary["favorite_orgs"][org] = activity_summary["favorite_orgs"].get(org, 0) + 1

            elif platform == "bluesky" and account.get("access_jwt") and account.get("did"):
                # Para BlueSky, podemos usar a API completa com autenticação
                data = self.get_bluesky_data(account["access_jwt"], account["did"])
                if "error" not in data:
                    # Contabilizar posts relacionados a esports
                    interactions = data["esports_posts"]["count"]
                    activity_summary["interactions"]["total"] += interactions
                    activity_summary["interactions"]["by_platform"]["bluesky"] = interactions

                    # Analisar organizações favoritas
                    for post in data["esports_posts"]["sample"]:
                        for org in self.esports_orgs:
                            if org in post["text"].lower():
                                activity_summary["favorite_orgs"][org] = activity_summary["favorite_orgs"].get(org, 0) + 1

        # Determinar nível de engajamento
        if activity_summary["interactions"]["total"] > 10:
            activity_summary["engagement_level"] = "high"
        elif activity_summary["interactions"]["total"] > 5:
            activity_summary["engagement_level"] = "medium"

        # Ordenar organizações favoritas
        activity_summary["favorite_orgs"] = dict(
            sorted(activity_summary["favorite_orgs"].items(),
                   key=lambda item: item[1],
                   reverse=True)
        )

        return activity_summary