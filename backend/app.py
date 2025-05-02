from fastapi import FastAPI, HTTPException, Request, Form, Body, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from database import Database
from document_validation import validate_documents, validate_rg
from esports_profile_validation import EsportsProfileValidator
from social_media_integration import SocialMediaIntegration
import os
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime

# Carregar variáveis do arquivo .env
load_dotenv()

# Inicializar o aplicativo FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar serviços
db = Database()
esports_validator = EsportsProfileValidator()
social_media = SocialMediaIntegration()

# Modelos de dados
class UserData(BaseModel):
    name: str
    email: str
    cpf: str
    birthdate: str
    address: str
    phone: str
    interests: List[str]
    teams: List[str]
    events: str
    purchases: str

class SocialAccount(BaseModel):
    platform: str
    username: str
    credentials: Optional[Dict] = None

class BlueskyCredentials(BaseModel):
    identifier: str
    password: str

# gerUserbyId
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """
    Retorna os dados de um usuário específico
    """
    from bson.objectid import ObjectId

    try:
        # Converter string para ObjectId
        user_id_obj = ObjectId(user_id)
        user = db.get_user(user_id_obj)

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Converter ObjectId para string para serialização JSON
        if '_id' in user:
            user['_id'] = str(user['_id'])

        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Rotas para dados do usuário
@app.post("/submit-user-data")
async def submit_user_data(user_data: UserData):
    # Aqui implementaremos a conexão com banco de dados
    result = db.save_user_data(user_data.dict())
    return {"status": "success", "data": user_data, "id": str(result.inserted_id)}

@app.post("/validate-rg")
async def validate_rg_endpoint(
    rg_document: UploadFile = File(...),
    user_id: str = Form(...)
):
    # Ler o arquivo de imagem
    document_bytes = await rg_document.read()

    # Validar o RG
    validation_result = validate_rg(document_bytes)

    # Se o RG for válido, atualizar o perfil do usuário
    if validation_result["valid"]:
        db.update_user_data(user_id, {
            "rg_verified": True,
            "rg_number": validation_result["rg_number"]
        })

    return validation_result

@app.post("/verify-identity")
async def verify_identity(
    document: UploadFile = File(...),
    selfie: UploadFile = File(...),
    user_id: str = Form(...)
):
    # Ler os arquivos de imagem
    document_bytes = await document.read()
    selfie_bytes = await selfie.read()

    # Validar o documento e a selfie
    validation_result = validate_documents(document_bytes, selfie_bytes)

    # Atualizar o status de verificação do usuário
    if validation_result.get("face_match", False):
        db.update_user_data(user_id, {"identity_verified": True})

    return validation_result

# Rota para obter todos os usuários (apenas para desenvolvimento)
@app.get("/users")
async def get_all_users():
    """
    Retorna todos os usuários registrados no banco de dados.
    ATENÇÃO: Esta rota é apenas para desenvolvimento e deve ser removida em produção.
    """
    users = db.get_all_users()
    return {
        "total": len(users),
        "users": users
    }

# Rotas para Bluesky
@app.post("/users/{user_id}/bluesky")
async def link_bluesky_account(user_id: str, credentials: BlueskyCredentials):
    """Vincula uma conta BlueSky ao perfil do usuário"""
    try:
        # Verificar se o usuário existe
        user = db.get_user_data(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Remover o @ do início do identificador, se presente
        identifier = credentials.identifier
        if identifier.startswith('@'):
            identifier = identifier[1:]

        # Prosseguir com a vinculação
        result = social_media.link_social_account(
            user_id,
            "bluesky",
            identifier,
            {"identifier": identifier, "password": credentials.password}
        )

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        # Atualizar o perfil do usuário no banco de dados
        db.update_user_social_account(user_id, {
            "platform": "bluesky",
            "username": identifier,
            **result["profile_data"]
        })

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/users/{user_id}/bluesky/update")
async def update_bluesky_account(user_id: str):
    """Atualiza os dados da conta BlueSky vinculada"""
    try:
        # Verificar se o usuário existe
        user = db.get_user_data(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Encontrar a conta do Bluesky vinculada
        bluesky_account = None
        for account in user.get("social_accounts", []):
            if account.get("platform") == "bluesky":
                bluesky_account = account
                break

        if not bluesky_account:
            raise HTTPException(status_code=404, detail="Conta BlueSky não encontrada")

        # Atualizar dados da conta
        result = social_media.update_bluesky_data(
            user_id,
            bluesky_account.get("did"),
            bluesky_account.get("access_jwt"),
            bluesky_account.get("refresh_jwt")
        )

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        # Atualizar o perfil do usuário no banco de dados
        db.update_user_social_account(user_id, {
            "platform": "bluesky",
            "username": bluesky_account.get("username"),
            **result["data"]
        })

        return {"status": "success", "message": "Dados da conta BlueSky atualizados com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}/social-accounts/{platform}")
async def unlink_social_account(user_id: str, platform: str):
    """Remove a vinculação de uma conta de rede social"""
    if platform != "bluesky":
        raise HTTPException(status_code=400, detail="Plataforma não suportada. Apenas Bluesky está disponível.")

    result = db.remove_user_social_account(user_id, platform)
    if not result:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    return {"status": "success", "message": f"Conta {platform} desvinculada com sucesso"}

@app.get("/users/{user_id}/esports-activity")
async def get_esports_activity(user_id: str):
    """Obtém um resumo das atividades relacionadas a esports do usuário"""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    linked_accounts = user.get("social_accounts", [])
    if not linked_accounts:
        return {"message": "Nenhuma conta de rede social vinculada"}

    activity = social_media.get_user_esports_activity(user_id, linked_accounts)
    return activity


# Modelo de dados para perfil de e-sports
class EsportsProfileLink(BaseModel):
    profile_url: HttpUrl
    notes: Optional[str] = None

# Rota para adicionar perfil de e-sports
@app.post("/users/{user_id}/esports-profiles")
async def add_esports_profile(user_id: str, profile: EsportsProfileLink):
    """
    Adiciona e valida um perfil de e-sports para o usuário
    """
    try:
        # Verificar se o usuário existe
        user = db.get_user_data(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Validar o perfil
        validation_result = esports_validator.validate_profile_url(str(profile.profile_url))

        if not validation_result.get("valid", False):
            return {
                "valid": False,
                "error": validation_result.get("error", "Perfil inválido")
            }

        # Analisar relevância do perfil para o usuário
        user_interests = user.get("interests", [])
        relevance_analysis = esports_validator.analyze_profile_relevance(validation_result, user_interests)

        # Preparar dados do perfil para salvar
        profile_data = {
            "profile_url": str(profile.profile_url),
            "platform": validation_result.get("platform"),
            "username": validation_result.get("nickname") or validation_result.get("username"),
            "validated_at": datetime.now().isoformat(),
            "validation_data": validation_result,
            "relevance": relevance_analysis,
            "notes": profile.notes
        }

        # Salvar o perfil no banco de dados
        if "esports_profiles" not in user:
            db.update_user_data(user_id, {"esports_profiles": []})

        # Verificar se o perfil já existe
        existing_profiles = user.get("esports_profiles", [])
        for i, existing_profile in enumerate(existing_profiles):
            if existing_profile.get("profile_url") == str(profile.profile_url):
                # Atualizar perfil existente
                existing_profiles[i] = profile_data
                db.update_user_data(user_id, {"esports_profiles": existing_profiles})
                return {
                    "valid": True,
                    "profile_data": validation_result,
                    "relevance": relevance_analysis,
                    "message": "Perfil de e-sports atualizado com sucesso"
                }

        # Adicionar novo perfil
        db.update_user_data(user_id, {"$push": {"esports_profiles": profile_data}})

        return {
            "valid": True,
            "profile_data": validation_result,
            "relevance": relevance_analysis,
            "message": "Perfil de e-sports adicionado com sucesso"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Rota para listar perfis de e-sports
@app.get("/users/{user_id}/esports-profiles")
async def get_user_esports_profiles(user_id: str):
    """
    Retorna todos os perfis de e-sports do usuário
    """
    user = db.get_user_data(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user.get("esports_profiles", [])

# Rota para validar perfil sem associar a um usuário
@app.post("/validate-esports-profile")
async def validate_esports_profile(profile: EsportsProfileLink):
    """
    Valida um perfil de e-sports sem associá-lo a um usuário
    """
    validation_result = esports_validator.validate_profile_url(str(profile.profile_url))

    return {
        "valid": validation_result.get("valid", False),
        "profile_data": validation_result if validation_result.get("valid", False) else None,
        "error": validation_result.get("error") if not validation_result.get("valid", False) else None
    }