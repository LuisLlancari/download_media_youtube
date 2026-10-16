# Usamos una imagen oficial ligera de Python
FROM python:3.11-slim

# Instalamos ffmpeg en el sistema operativo del contenedor
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos e instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente del backend
COPY app/ ./app/

# Copiamos el frontend (docs) para servirlo como archivos estáticos
COPY docs/ ./docs/

# Puerto por defecto (se puede sobreescribir con la variable PORT)
EXPOSE 8000

# Levantamos el servidor uvicorn
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"