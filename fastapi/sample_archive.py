from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # Permet l'accès depuis n'importe quelle origine. À restreindre en production
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Informations Keycloak
KEYCLOAK_URL = "http://localhost:8080/auth/realms/master"
CLIENT_ID = "recipe"
CLIENT_SECRET = "p1dPEWjPu5H0ce16UvgGWc3AExSYIB1a"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = f"{KEYCLOAK_URL}/protocol/openid-connect/token")


class User(BaseModel):
    username: str
    roles: List[str] = []


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    headers = {"Authorization": f"Bearer {token}"}
    # Requête vers Keycloak pour vérifier le token et récupérer les informations de l'utilisateur
    response = requests.get(f"{KEYCLOAK_URL}/protocol/openid-connect/userinfo", headers = headers)
    if response.status_code != 200:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid token")

    user_info = response.json()
    return User(username = user_info["preferred_username"], roles = user_info.get("roles", []))


@app.get("/protected-route")
def protected_route(user: User = Depends(get_current_user)):
    return {"message": f"Hello {user.username}, you have access!"}
