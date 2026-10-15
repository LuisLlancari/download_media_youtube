
import os
import uuid
import time
import yt_dlp
from app.utils import sanitize_filename

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

MAX_DURATION_SECONDS = 1800


def download_video(url: str, quality: str = "720", duration: int = None, title: str = None) -> dict:
    # Normalizar calidad: "720p" -> "720"
    res = quality.lower().replace("p", "").strip()

    if not res.isdigit():
        raise ValueError("La calidad seleccionada no es válida.")

    res = int(res)

    # Obtener información y validar duración
    with yt_dlp.YoutubeDL({
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 15,
        "retries": 1,
        "extractor_retries": 1,
    }) as ydl:
        info = ydl.extract_info(url, download=False)

    duration = info.get("duration") or 0
    raw_title = title or info.get("title") or "video_youtube"
    final_title = sanitize_filename(raw_title)

    if duration > MAX_DURATION_SECONDS:
        raise ValueError(
            f"El video dura {duration // 60} minutos. "
            f"El límite máximo permitido es "
            f"{MAX_DURATION_SECONDS // 60} minutos."
        )

    file_id = str(uuid.uuid4())
    output_template = os.path.join(
        DOWNLOAD_DIR, f"{file_id}.%(ext)s"
    )

    # Primero intenta la resolución exacta.
    # Si no existe, selecciona la mejor resolución inferior.
    format_spec = (
        f"bestvideo[height={res}]+bestaudio/"
        f"best[height={res}]/"
        f"bestvideo[height<={res}]+bestaudio/"
        f"best[height<={res}]"
    )

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 30,
        "retries": 2,
        "extractor_retries": 2,
        "format": format_spec,
        "outtmpl": output_template,
        "merge_output_format": "mp4",
    }

    # Descargar el video y obtener la ruta final.
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        downloaded_info = ydl.extract_info(url, download=True)

        filepath = downloaded_info.get("filepath")

        # Alternativa por si yt-dlp no devuelve la ruta final.
        if not filepath or not os.path.isfile(filepath):
            candidates = [
                os.path.join(DOWNLOAD_DIR, f)
                for f in os.listdir(DOWNLOAD_DIR)
                if f.startswith(file_id + ".")
                and os.path.isfile(os.path.join(DOWNLOAD_DIR, f))
                and not f.endswith((".part", ".ytdl"))
            ]

            if not candidates:
                raise FileNotFoundError(
                    "No se encontró el archivo descargado."
                )

            filepath = candidates[0]

    return {
        "filepath": filepath,
        "title": final_title,
        "extension": os.path.splitext(filepath)[1].lstrip("."),
    }
