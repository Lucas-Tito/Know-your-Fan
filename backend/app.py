from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List
import uvicorn
from document_validation import validate_rg
from database import Database

app = FastAPI()
db = Database()

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
    from document_validation import validate_documents
    validation_result = validate_documents(document_bytes, selfie_bytes)

    # Atualizar o status de verificação do usuário
    if validation_result.get("face_match", False):
        db.update_user_data(user_id, {"identity_verified": True})

    return validation_result