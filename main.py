import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title = "Keycloak Authentication API",
    description = "Retrieve a token via Keycloak to access other APIs."
)

KEYCLOAK_URL = os.environ['KEYCLOAK_URL']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/token", response_model = Token, tags = ["Authentication"])
def get_token(username: str, password: str):
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    response = requests.post(f"{KEYCLOAK_URL}/token", data = payload)
    if response.status_code != 200:
        raise HTTPException(status_code = 401, detail = "Invalid credentials")
    return response.json()
