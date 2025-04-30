from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

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
    return {"status": "success", "data": user_data}