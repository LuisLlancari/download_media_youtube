import yt_dlp
import os
import uuid
import glob

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Límite de seguridad: 30 minutos (1800 segundos)
MAX_DURATION_SECONDS = 1800 

def download_video(url: str, quality: str = "720", duration: int = None) -> dict:
    """
    Descarga el video de YouTube en la resolución seleccionada en formato MP4.
    """
    # 1. Si no nos pasan la duración, la obtenemos para validar
    if duration is None:
        with yt_dlp.YoutubeDL({'noplaylist': True, 'skip_download': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)
            title = info.get('title', 'video_youtube')
    else:
        title = "video_youtube"

    # Validar límite de duración
    if duration > MAX_DURATION_SECONDS:
        raise ValueError(f"El video dura {duration // 60} minutos. El límite máximo permitido es de {MAX_DURATION_SECONDS // 60} minutos.")

    file_id = str(uuid.uuid4())
    
    # Limpiamos el texto de calidad si viene como "720p" para dejar solo "720"
    res = quality.lower().replace("p", "").strip()

    # Regla de formato: busca la resolución específica o la mejor disponible por debajo de ella
    if res.isdigit():
        format_spec = (
            f"bestvideo[height<={res}]+bestaudio/"
            f"best[height<={res}]"
        )
    else:
        format_spec = "bestvideo+bestaudio/best"


    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/{file_id}.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'format': format_spec,
        'merge_output_format': 'mp4',

        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'] 
            }
        },
        'nocheckcertificate': True
    }

    # 2. Ejecutar la descarga
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_download = ydl.extract_info(url, download=True)
        title = info_download.get('title', title)

    downloaded_files = glob.glob(f"{DOWNLOAD_DIR}/{file_id}.*")
    if not downloaded_files:
        raise Exception("No se pudo generar el archivo MP4.")

    return {
        "filepath": downloaded_files[0],
        "title": title,
        "extension": "mp4"
    }