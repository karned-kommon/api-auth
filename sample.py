from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import requests
from jose import jwt, JWTError

app = FastAPI()

# Configuration Keycloak
KEYCLOAK_URL = "https://iam.karned.bzh/realms/Karned/protocol/openid-connect"
CLIENT_ID = "api-recipe"
CLIENT_SECRET = "e5z4BLTi7qdn4ZndNqQsDR9sdAVlisnT"

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/token", response_model=Token)
def get_token(username: str, password: str):
    """Obtenir un token depuis Keycloak"""
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    response = requests.post(f"{KEYCLOAK_URL}/token", data=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return response.json()


def verify_token(token: str):
    """Vérifier et décoder le token JWT"""
    try:
        openid_config = requests.get(f"{KEYCLOAK_URL}/.well-known/openid-configuration").json()
        jwks_uri = openid_config["jwks_uri"]
        jwks = requests.get(jwks_uri).json()
        key = next((key for key in jwks["keys"] if key["alg"] == "RS256"), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token signing key")
        public_key = jwt.construct_rsa_key(key)
        decoded_token = jwt.decode(token, public_key, algorithms=["RS256"], audience=CLIENT_ID)
        return decoded_token
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    """Exemple de route protégée"""
    decoded_token = verify_token(token)
    return {"message": "You have access to this route!", "user": decoded_token["preferred_username"]}