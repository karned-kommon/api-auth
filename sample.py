from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic import BaseModel
import requests
from jose import jwt, JWTError, jwk
import logging

# Configurez le logger pour afficher les informations dans la console
logging.basicConfig(level=logging.DEBUG)


app = FastAPI()

# Configuration Keycloak
KEYCLOAK_URL = "https://iam.karned.bzh/realms/Karned/protocol/openid-connect"
CLIENT_ID = "api-recipe"
CLIENT_SECRET = "e5z4BLTi7qdn4ZndNqQsDR9sdAVlisnT"

# OAuth2 configuration (cela ne sera plus utilisé dans Swagger directement)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Nouvelle configuration de sécurité pour Bearer Token dans Swagger
http_bearer = HTTPBearer()

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
        # Récupérer la configuration OpenID de Keycloak
        openid_config = requests.get(f"https://iam.karned.bzh/realms/Karned/.well-known/openid-configuration").json()
        jwks_uri = openid_config["jwks_uri"]
        logging.debug(f"Récupération des clés publiques depuis {jwks_uri}")

        # Récupérer les clés JWKS
        jwks = requests.get(jwks_uri).json()
        logging.debug(f"Clés JWKS récupérées : {jwks}")

        # Trouver la clé publique qui correspond au JWT
        key = next((key for key in jwks["keys"] if key["alg"] == "RS256"), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token signing key")

        logging.debug(f"Clé publique trouvée : {key}")

        # Construire la clé publique RSA
        public_key = jwk.construct(key)  # Utilisation de jwk.construct() pour créer la clé RSA
        logging.debug(f"Clé publique construite : {public_key}")

        decoded_token = jwt.decode(token, public_key, algorithms=["RS256"], audience=CLIENT_ID)
        logging.debug(f"Token décodé : {decoded_token}")
        logging.debug(f"Audience du token : {decoded_token.get('aud')}")

        # Vérifier l'audience du token (doit correspondre à CLIENT_ID)
        if decoded_token.get("aud") != CLIENT_ID:
            raise HTTPException(status_code=401, detail="Invalid audience")

        return decoded_token
    except JWTError as e:
        logging.error(f"Erreur de décodage du token JWT : {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"Erreur lors de la vérification du token : {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/protected")
def protected_route(token: str = Depends(http_bearer)):
    """Exemple de route protégée"""
    decoded_token = verify_token(token.credentials)
    return {"message": "You have access to this route!", "user": decoded_token["preferred_username"]}