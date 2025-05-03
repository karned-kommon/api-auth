from fastapi import APIRouter

from config.config import API_TAG_NAME
from models.item_model import LoginRequest, Token
from services.item_service import get_keycloak_token

VERSION = "v1"
api_group_name = f"/{API_TAG_NAME}/{VERSION}/"

router = APIRouter(
    tags=[api_group_name],
    prefix=f"/auth/{VERSION}"
)

@router.post("/token", response_model=Token)
async def get_token(login_request: LoginRequest):
    return await get_keycloak_token(login_request)