# 🎵 YouTube Media Downloader

Aplicación para descargar música y videos de YouTube. Está compuesta por un **backend** (API REST con FastAPI) y un **frontend** (interfaz web estática servida desde la misma instancia).

---

## 🗂️ Estructura del Proyecto

```
download_media_api/
├── app/                    # Backend (FastAPI)
│   ├── main.py             # Punto de entrada, rutas principales
│   ├── config.py           # CORS y configuración de archivos estáticos
│   ├── schemas.py          # Modelos de datos (Pydantic)
│   ├── utils.py            # Utilidades generales
│   └── services/
│       ├── info_service.py     # Obtiene información del video
│       ├── audio_service.py    # Descarga de audio
│       └── video_service.py    # Descarga de video
├── docs/                   # Frontend (HTML + JS estático)
│   ├── index.html          # Interfaz de usuario
│   └── js/
│       ├── config.js       # URL base del API
│       ├── api.request.js  # Llamadas HTTP al backend
│       └── page.js         # Lógica de la página
├── downloads/              # Carpeta temporal de archivos descargados
├── requirements.txt        # Dependencias de Python
└── Dockerfile              # Configuración de Docker
```

---

## ⚙️ ¿Cómo funciona?

1. El usuario ingresa una URL de YouTube en el frontend.
2. El frontend consulta el endpoint `/info` del backend para obtener los formatos disponibles (audio y video).
3. El usuario selecciona la calidad deseada y hace clic en **Descargar**.
4. El backend descarga el archivo mediante `yt-dlp`, lo convierte con `ffmpeg` y lo devuelve como respuesta HTTP.
5. El archivo se elimina automáticamente del servidor tras ser enviado.

### Endpoints del API

| Método | Ruta               | Descripción                                |
|--------|--------------------|--------------------------------------------|
| GET    | `/health`          | Verifica que el servidor está activo       |
| POST   | `/info`            | Obtiene información y formatos del video   |
| POST   | `/download/audio`  | Descarga el audio en el bitrate indicado   |
| POST   | `/download/video`  | Descarga el video en la calidad indicada   |

---

## 🐳 Levantar el Proyecto con Docker

Este es el método recomendado. Con un solo contenedor se levanta tanto el **backend** como el **frontend**.

### Requisitos previos

- [Docker](https://www.docker.com/get-started) instalado y en ejecución.

### Pasos

**1. Clonar el repositorio**

```bash
git clone https://github.com/LuisLlancari/download_media_youtube.git
cd download_media_youtube
```

**2. Construir la imagen Docker**

```bash
docker build -t youtube-downloader .
```

**3. Ejecutar el contenedor**

```bash
docker run -p 8000:8000 youtube-downloader
```

**4. Abrir en el navegador**

```
http://localhost:8000
```

El frontend se carga automáticamente desde la raíz y se comunica con el API en el mismo puerto.

### Variables de entorno

| Variable | Valor por defecto | Descripción                          |
|----------|-------------------|--------------------------------------|
| `PORT`   | `8000`            | Puerto en el que corre el servidor   |

Para usar un puerto diferente:

```bash
docker run -p 9090:9090 -e PORT=9090 youtube-downloader
```

---

## 💻 Levantar en Modo Desarrollo (sin Docker)

### Requisitos previos

- Python 3.11+
- `ffmpeg` instalado en el sistema ([instrucciones](https://ffmpeg.org/download.html))

### Pasos

**1. Crear y activar el entorno virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

**2. Instalar las dependencias**

```bash
pip install -r requirements.txt
```

**3. Levantar el servidor**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**4. Acceder a la aplicación**

Abre el navegador en:

```
http://localhost:8000
```

> El archivo `docs/js/config.js` apunta a `http://127.0.0.1:8000` por defecto, así que no necesitas cambiar nada.

---

## 🛠️ Tecnologías Utilizadas

| Capa      | Tecnología                              |
|-----------|-----------------------------------------|
| Backend   | Python 3.11, FastAPI, uvicorn           |
| Descarga  | yt-dlp, ffmpeg                          |
| Frontend  | HTML5, Bootstrap 5, JavaScript (ES6+)   |
| Contenedor| Docker                                  |

---

## 📝 Notas

- Los archivos descargados se eliminan automáticamente del servidor tras ser entregados al cliente.
- No se almacena ningún dato del usuario ni historial de descargas.
