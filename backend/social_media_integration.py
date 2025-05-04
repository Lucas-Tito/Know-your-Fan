import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

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
            platform: Plataforma (bluesky)
            username: Nome de usuário na plataforma
            credentials: Credenciais para plataformas que exigem (como BlueSky)

        Returns:
            dict: Status da vinculação e dados básicos do perfil
        """
        try:
            if platform == "bluesky":
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
                return {"status": "error", "message": "Plataforma não suportada. Apenas Bluesky está disponível."}

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
                },
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    def refresh_bluesky_token(self, refresh_jwt):
        """
        Atualiza o token JWT do BlueSky
        """
        try:
            refresh_url = f"{self.bluesky_server}/xrpc/com.atproto.server.refreshSession"
            headers = {"Authorization": f"Bearer {refresh_jwt}"}

            response = requests.post(refresh_url, headers=headers)
            refresh_data = response.json()

            if 'error' in refresh_data:
                return {"status": "error", "message": refresh_data.get('error', 'Erro ao atualizar token')}

            return {
                "status": "success",
                "access_jwt": refresh_data.get('accessJwt'),
                "refresh_jwt": refresh_data.get('refreshJwt')
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_bluesky_data(self, user_id, did, access_jwt, refresh_jwt=None):
        """
        Atualiza os dados do usuário no BlueSky
        """
        try:
            # Verificar se o token expirou e tentar atualizar
            profile_url = f"{self.bluesky_server}/xrpc/app.bsky.actor.getProfile"
            headers = {"Authorization": f"Bearer {access_jwt}"}
            params = {"actor": did}

            profile_response = requests.get(profile_url, headers=headers, params=params)

            # Se o token expirou e temos um refresh token, tentar atualizar
            if profile_response.status_code == 401 and refresh_jwt:
                refresh_result = self.refresh_bluesky_token(refresh_jwt)
                if refresh_result["status"] == "error":
                    return refresh_result

                access_jwt = refresh_result["access_jwt"]
                refresh_jwt = refresh_result["refresh_jwt"]
                headers = {"Authorization": f"Bearer {access_jwt}"}
                profile_response = requests.get(profile_url, headers=headers, params=params)

            if profile_response.status_code != 200:
                return {"status": "error", "message": f"Erro ao obter perfil: {profile_response.text}"}

            # Obter dados atualizados
            updated_data = self.get_bluesky_data(access_jwt, did)

            if "error" in updated_data:
                return {"status": "error", "message": updated_data["error"]}

            # Adicionar tokens atualizados
            updated_data["access_jwt"] = access_jwt
            updated_data["refresh_jwt"] = refresh_jwt
            updated_data["did"] = did

            return {"status": "success", "data": updated_data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_user_esports_activity(self, user_id, linked_accounts):
        """
        Obtém os dados detalhados da conta Bluesky vinculada do usuário,
        incluindo perfil e posts relacionados a esports, similar à função link_social_account.
        """
        for account in linked_accounts:
            if account.get("access_jwt") and account.get("did"):
                # Obter dados completos do Bluesky com autenticação
                data = self.get_bluesky_data(account["access_jwt"], account["did"])
                if "error" not in data:
                    # Adicionar tokens e DID para manter compatibilidade
                    data["access_jwt"] = account["access_jwt"]
                    data["refresh_jwt"] = account.get("refresh_jwt", "")
                    data["did"] = account["did"]
                    return {
                        "status": "success",
                        "message": "success retrieving data",
                        "profile_data": data
                    }
                else:
                    return {
                        "status": "error",
                        "message": data["error"]
                    }
        # Caso não encontre conta Bluesky válida
        return {
            "status": "error",
            "message": "Conta Bluesky não vinculada ou tokens inválidos"
        }