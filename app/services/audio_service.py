import yt_dlp
import os
import uuid
import glob
from app.utils import sanitize_filename

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_audio(url: str, bitrate: str = "192", title: str = None) -> dict:
    """
    Descarga el audio de una URL de YouTube y lo convierte a MP3.
    """

    final_title = sanitize_filename(title) if title else None

    file_id = str(uuid.uuid4())
    
    # Configuración de yt-dlp + FFmpeg para extracción de MP3
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

    # Ejecutar la descarga y conversión 
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_download = ydl.extract_info(url, download=True)
        
        # Si no nos pasaron título al principio
        if not final_title:
            raw_title = info_download.get('title', 'audio_youtube')
            final_title = sanitize_filename(raw_title)

    downloaded_files = glob.glob(f"{DOWNLOAD_DIR}/{file_id}.*")
    if not downloaded_files:
        raise Exception("No se pudo generar el archivo MP3.")

    return {
        "filepath": downloaded_files[0],
        "title": final_title,
        "extension": "mp3"
    }