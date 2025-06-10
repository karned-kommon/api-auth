from fastapi import APIRouter

from config.config import API_TAG_NAME
from models.item_model import LoginRequest, Token, TokenRenewRequest
from models.response_model import SuccessResponse, create_success_response
from services.item_service import get_keycloak_token, renew_keycloak_token

VERSION = "v1"
api_group_name = f"/{API_TAG_NAME}/{VERSION}/"

router = APIRouter(
    tags=[api_group_name],
    prefix=f"/auth/{VERSION}"
)

@router.post("/token", response_model=SuccessResponse[Token])
async def get_token(login_request: LoginRequest):
    token = await get_keycloak_token(login_request)
    return create_success_response(token)

@router.post("/renew", response_model=SuccessResponse[Token])
async def renew_token(renew_request: TokenRenewRequest):
    token = await renew_keycloak_token(renew_request)
    return create_success_response(token)
