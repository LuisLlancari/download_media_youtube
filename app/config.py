from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Dominios permitidos para consumir tu API
# Puedes reemplazar "*" por la URL exacta de tu GitHub Pages cuando la tengas publicada:
# ej. ["https://tu-usuario.github.io"]
ORIGINS = ["*"]

def setup_cors(app: FastAPI) -> None:
    """Configura los middlewares de CORS en la instancia de FastAPI."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition", "X-Filename"],
    )