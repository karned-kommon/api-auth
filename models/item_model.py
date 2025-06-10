from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenRenewRequest(BaseModel):
    refresh_token: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str = None
