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
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import Form
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from bson.objectid import ObjectId

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
    password: str

class SocialAccount(BaseModel):
    platform: str
    username: str
    credentials: Optional[Dict] = None

class BlueskyCredentials(BaseModel):
    identifier: str
    password: str

class LoginForm(BaseModel):
    email: str
    password: str    

class SteamProfile(BaseModel):
    profile_url: str

# Configurações para JWT
SECRET_KEY = os.getenv('SECRET_KEY')  # Troque para uma chave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    print(f"Tentando verificar senha. Hash armazenado: {hashed_password}")
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Erro ao verificar senha: {e}")
        return False

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str):
    user = db.get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.get("hashed_password", "")):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user["_id"] = str(user["_id"])
    return user


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

@app.post("/submit-user-data")
async def submit_user_data(user_data: UserData):
    # Hash da senha antes de salvar
    hashed_password = get_password_hash(user_data.password)
    user_data_dict = user_data.dict()
    user_data_dict["hashed_password"] = hashed_password
    del user_data_dict["password"]  # Remover o campo de senha em texto puro

    # Aqui implementaremos a conexão com banco de dados
    result = db.save_user_data(user_data_dict)  # <-- CORRIGIDO!
    return {"status": "success", "data": user_data, "id": str(result.inserted_id)}

@app.post("/validate-rg")
async def validate_rg_endpoint(
    rg_document: UploadFile = File(...),
    # user_id: str = Form(...)
):
    # Ler o arquivo de imagem
    document_bytes = await rg_document.read()

    # Validar o RG
    validation_result = validate_rg(document_bytes)

    # # Se o RG for válido, atualizar o perfil do usuário
    # if validation_result["valid"]:
    #     db.update_user_data(user_id, {
    #         "rg_verified": True,
    #         "rg_number": validation_result["rg_number"]
    #     })

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
@app.post("/users/{user_id}/validate_esports_profile_relevance")
async def validate_profile(user_id: str, profile: EsportsProfileLink):
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
        relevance_analysis = await esports_validator.analyze_profile_relevance(validation_result, user_interests)

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
        db.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"esports_profiles": profile_data}}
        )

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
    user_data = db.get_user_data(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    profile_url = user_data.get("profile_url")
    if not profile_url:
        raise HTTPException(status_code=404, detail="Perfil Steam não vinculado")
    
    return {"profile_url": profile_url}

@app.post("/users/{user_id}/esports-profiles")
async def link_steam_profile(user_id: str, profile: SteamProfile):
    updated = db.update_user_data(user_id, {
        "profile_url": profile.profile_url,
        "platform": "steam"  # Adiciona ou atualiza o campo "platform" com o valor "steam"
    })
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou erro ao atualizar")
    return {"status": "success", "profile_url": profile.profile_url}

# Rota para validar perfil sem associar a um usuário
@app.post("/validate-esports-profile")
async def validate_esports_profile(
    profile: EsportsProfileLink,
    user_id: Optional[str] = None
):
    """
    Valida um perfil de e-sports com análise de IA
    """
    validation_result = esports_validator.validate_profile_url(str(profile.profile_url))

    if not validation_result.get("valid", False):
        return {
            "valid": False,
            "error": validation_result.get("error", "Perfil inválido")
        }

    # Obter interesses do usuário se disponível
    user_interests = []
    if user_id:
        user = db.get_user_data(user_id)
        user_interests = user.get("interests", [])

    # Análise de relevância com IA
    relevance = await esports_validator.analyze_profile_relevance(
        validation_result,
        user_interests
    )

    return {
        "valid": True,
        "profile_data": validation_result,
        "relevance_analysis": relevance
    }