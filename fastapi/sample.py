from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import requests

app = FastAPI()


# URL d'authentification Keycloak
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8080/auth/realms/master/protocol/openid-connect/token")

@app.get("/protected-route")
def protected_route(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"http://localhost:8080/auth/realms/myrealm/protocol/openid-connect/userinfo", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": "Access granted"}