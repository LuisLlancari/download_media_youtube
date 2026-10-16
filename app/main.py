from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import os

from app.config import setup_cors, setup_static_files
from app.schemas import InfoRequest, AudioRequest, VideoRequest
from app.services.info_service import get_video_info
from app.services.audio_service import download_audio
from app.services.video_service import download_video
from app.utils import build_content_disposition
from urllib.parse import quote

app = FastAPI(title="YouTube Downloader API")

# Inicializamos la configuración de CORS
setup_cors(app)

def cleanup_file(filepath: str):
    """Elimina el archivo del servidor de forma asíncrona tras la descarga."""
    if os.path.exists(filepath):
        os.remove(filepath)

# Endpoint para obtener información del video
@app.post("/info")
async def info_endpoint(request: InfoRequest):
    try:
        print(f"Buscando")
        return get_video_info(request.url)
        print(f"Información obtenida ")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo obtener información del video: {str(e)}")

# Endpoint para descargar audio
@app.post("/download/audio")
async def download_audio_endpoint(request: AudioRequest, background_tasks: BackgroundTasks):
    try:
        result = download_audio(url=request.url, bitrate=request.bitrate, title=request.title)
        background_tasks.add_task(cleanup_file, result["filepath"])
        
        disposition, full_name = build_content_disposition(result["title"], result["extension"])
        
        return FileResponse(
            path=result["filepath"],
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": disposition,
                "X-Filename": quote(full_name, encoding="utf-8"),
            }
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para descargar video
@app.post("/download/video")
async def download_video_endpoint(request: VideoRequest, background_tasks: BackgroundTasks):
    try:
        result = download_video(url=request.url, quality=request.quality, title=request.title)
        background_tasks.add_task(cleanup_file, result["filepath"])
        
        disposition, full_name = build_content_disposition(result["title"], result["extension"])
        
        return FileResponse(
            path=result["filepath"],
            media_type="video/mp4",
            headers={
                "Content-Disposition": disposition,
                "X-Filename": quote(full_name, encoding="utf-8"),
            }
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "API activa y modularizada."}

# Montamos el frontend estático al final para no interceptar las rutas del API
setup_static_files(app)