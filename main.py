import logging

from fastapi import FastAPI
from routers import v1

logging.basicConfig(level=logging.INFO)
logging.info("Starting API Auth")

app = FastAPI(
    title="API Auth",
    description="Retrieve a token via Keycloak to access other APIs.",
    openapi_url="/auth/openapi.json"
)

# Include routers
app.include_router(v1.router)
