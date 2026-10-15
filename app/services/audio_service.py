import yt_dlp
import os
import uuid
import glob

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Límite de seguridad: 30 minutos (1800 segundos)
MAX_DURATION_SECONDS = 1800 

def download_audio(url: str, bitrate: str = "192", duration: int = None) -> dict:
    """
    Descarga el audio de una URL de YouTube y lo convierte a MP3.
    """
    # 1. Si no nos pasan la duración desde el frontend, la consultamos rápidamente
    if duration is None:
        with yt_dlp.YoutubeDL({'noplaylist': True, 'skip_download': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)
            title = info.get('title', 'audio_youtube')
    else:
        # Si ya se validó antes, obtenemos el título directamente al descargar
        title = "audio_youtube"

    # Validar límite de duración para evitar saturar el disco de Koyeb
    if duration > MAX_DURATION_SECONDS:
        raise ValueError(f"El audio dura {duration // 60} minutos. El límite máximo permitido es de {MAX_DURATION_SECONDS // 60} minutos.")

    file_id = str(uuid.uuid4())
    
    # 2. Configuración de yt-dlp + FFmpeg para extracción de MP3
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/{file_id}.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': bitrate,
        }],
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'] 
            }
        },
        'nocheckcertificate': True
    }

    # 3. Ejecutar la descarga y conversión
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_download = ydl.extract_info(url, download=True)
        title = info_download.get('title', title)

    downloaded_files = glob.glob(f"{DOWNLOAD_DIR}/{file_id}.*")
    if not downloaded_files:
        raise Exception("No se pudo generar el archivo MP3.")

    return {
        "filepath": downloaded_files[0],
        "title": title,
        "extension": "mp3"
    }