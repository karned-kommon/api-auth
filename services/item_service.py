import httpx
from fastapi import HTTPException
from config.config import KEYCLOAK_URL, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET
from models.item_model import LoginRequest, Token, TokenRenewRequest

async def get_keycloak_token(login_request: LoginRequest) -> Token:
    payload = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
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
        return Token(
            access_token=token_data.get("access_token"),
            token_type=token_data.get("token_type"),
            refresh_token=token_data.get("refresh_token")
        )

async def renew_keycloak_token(renew_request: TokenRenewRequest) -> Token:
    payload = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": renew_request.refresh_token,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{KEYCLOAK_URL}/token", data=payload)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Keycloak server unreachable: {exc}")

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        token_data = response.json()
        return Token(
            access_token=token_data.get("access_token"),
            token_type=token_data.get("token_type"),
            refresh_token=token_data.get("refresh_token")
        )
