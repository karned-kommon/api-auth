import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(
    title="Keycloak Authentication API",
    description="Retrieve a token via Keycloak to access other APIs."
)

# Chargement des variables d'environnement avec vérification
KEYCLOAK_URL = os.getenv('KEYCLOAK_URL')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

if not all([KEYCLOAK_URL, CLIENT_ID, CLIENT_SECRET]):
    raise ValueError("Missing one or more environment variables: KEYCLOAK_URL, CLIENT_ID, CLIENT_SECRET")

if not KEYCLOAK_URL.rstrip('/').endswith('/protocol/openid-connect'):
    KEYCLOAK_URL = KEYCLOAK_URL.rstrip('/') + '/protocol/openid-connect'

# Modèle pour les données d'entrée
class LoginRequest(BaseModel):
    username: str
    password: str

# Modèle pour la réponse
class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/auth/token", response_model=Token, tags=["Authentication"])
async def get_token(login_request: LoginRequest):
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "password",
        "username": login_request.username,
        "password": login_request.password,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{KEYCLOAK_URL}/token", data=payload)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Keycloak server unreachable: {exc}")

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token_data = response.json()
        return {
            "access_token": token_data.get("access_token"),
            "token_type": token_data.get("token_type")
        }
