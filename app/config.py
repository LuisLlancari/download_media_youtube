from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Dominios permitidos para consumir el API -> * todos
ORIGINS = ["*"]

# middlewares en la instancia de fastAPI
def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ORIGINS,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
        expose_headers = ["Content-Disposition", "X-Filename"],
    )