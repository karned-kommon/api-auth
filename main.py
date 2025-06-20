import logging

from fastapi import FastAPI, HTTPException

from middlewares.cors_middleware import CORSMiddleware
from middlewares.exception_handler import http_exception_handler
from routers import v1

logging.basicConfig(level=logging.INFO)
logging.info("Starting API Auth")

app = FastAPI(
    title="API Auth",
    description="Retrieve a token via Keycloak to access other APIs.",
    openapi_url="/auth/openapi.json"
)


app.add_middleware(CORSMiddleware)
app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(v1.router)
