
import time
import yt_dlp


def get_video_info(url: str) -> dict:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 15,
        "retries": 1,
        "extractor_retries": 1,
        "skip_download": True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'] 
                }
        },
        'nocheckcertificate': True
    }

    start = time.perf_counter()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

    except Exception as e:
        raise ValueError(
            f"No se pudo obtener la información del video: {e}"
        ) from e

    elapsed = time.perf_counter() - start
    print(f"[yt-dlp] Información obtenida en {elapsed:.2f} segundos")

    duration = info.get("duration") or 0
    title = info.get("title") or "Sin título"
    thumbnail = info.get("thumbnail") or ""

    # Agrupar los formatos de video por resolución.
    heights_map = {}

    for fmt in info.get("formats", []):
        height = fmt.get("height")
        vcodec = fmt.get("vcodec")

        if not height or height <= 0:
            continue

        if not vcodec or vcodec == "none":
            continue

        filesize = fmt.get("filesize")

        if filesize is None:
            filesize = fmt.get("filesize_approx")

        bitrate = fmt.get("vbr") or fmt.get("tbr") or 0

        current = heights_map.get(height)

        if current is None or bitrate > current["bitrate"]:
            heights_map[height] = {
                "filesize": filesize,
                "bitrate": bitrate,
            }

    # Construir las resoluciones disponibles.
    video_qualities = []

    for height in sorted(heights_map):
        filesize = heights_map[height]["filesize"]

        video_qualities.append({
            "resolution": f"{height}p",
            "height": height,
            "ext": "mp4",
            "filesize_mb": (
                round(filesize / (1024 * 1024), 1)
                if filesize is not None
                else None
            ),
        })

    return {
        "title": title,
        "duration_seconds": duration,
        "duration_formatted": f"{duration // 60}:{duration % 60:02d}",
        "thumbnail": thumbnail,
        "video_qualities": video_qualities,
        "audio_options": [
            {
                "label": "MP3 Calidad Estándar (128 kbps)",
                "bitrate": "128",
            },
            {
                "label": "MP3 Alta Calidad (192 kbps)",
                "bitrate": "192",
            },
            {
                "label": "MP3 Máxima Calidad (320 kbps)",
                "bitrate": "320",
            },
        ],
    }
