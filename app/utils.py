import re
import unicodedata
from urllib.parse import quote


def sanitize_filename(title: str, max_length: int = 120) -> str:
    """
    Limpia un título para que sea un nombre de archivo válido y seguro en cualquier sistema operativo.
    Remueve caracteres prohibidos en Windows/Linux/macOS: \ / : * ? " < > | y caracteres de control.
    """
    if not title:
        return "media"

    # Reemplazar caracteres no válidos en sistemas de archivos y cabeceras
    cleaned = re.sub(r'[\\/*?:"<>|\x00-\x1f]', "", title)

    # Reemplazar múltiples espacios por uno solo
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Quitar puntos o espacios al final (problemáticos en Windows)
    cleaned = cleaned.rstrip(". ")

    if not cleaned:
        cleaned = "media"

    return cleaned[:max_length].rstrip(". ")


def build_content_disposition(filename_base: str, extension: str) -> tuple[str, str]:
    """
    Genera la cabecera Content-Disposition según RFC 6266 / RFC 5987 con:
    1. Fallback ASCII seguro: filename="nombre.mp4" (para navegadores y clientes básicos).
    2. Versión UTF-8 completa: filename*=utf-8''nombre%C3%A1.mp4 (para clientes modernos).

    Retorna una tupla: (content_disposition_header_value, clean_full_filename)
    """
    safe_base = sanitize_filename(filename_base)
    ext = extension.lstrip(".")
    full_name = f"{safe_base}.{ext}"

    # Generar versión ASCII segura para clientes antiguos o regex simples en frontend
    ascii_base = (
        unicodedata.normalize("NFKD", safe_base)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    ascii_base = re.sub(r"[^a-zA-Z0-9_\-\. ]", "", ascii_base).strip()
    if not ascii_base:
        ascii_base = "download"

    ascii_filename = f"{ascii_base}.{ext}"

    # Codificación UTF-8 para filename*=
    encoded_filename = quote(full_name, encoding="utf-8")

    disposition = (
        f'attachment; filename="{ascii_filename}"; filename*=utf-8\'\'{encoded_filename}'
    )
    return disposition, full_name
