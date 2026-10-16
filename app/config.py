from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Dominios permitidos para consumir el API
# Incluye GitHub Pages y acceso local (Docker / desarrollo)
ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

# middlewares en la instancia de fastAPI
def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition", "X-Filename"],
    )

def setup_static_files(app: FastAPI):
    """Monta el frontend (docs/) como archivos estáticos si la carpeta existe."""
    docs_path = os.path.join(os.path.dirname(__file__), "..", "docs")
    docs_path = os.path.abspath(docs_path)
    if os.path.isdir(docs_path):
        app.mount("/", StaticFiles(directory=docs_path, html=True), name="frontend")
