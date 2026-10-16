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

# Copiamos todo el código fuente de la aplicación al contenedor
COPY . .

# Exponemos el puerto que utiliza Koyeb por defecto
EXPOSE 8000

# Comando para arrancar la aplicación con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]