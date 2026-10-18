import re


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
    Genera la cabecera Content-Disposition con filename= usando el nombre completo.
    Se evita filename*= para que clientes como axios o browsers no concatenen
    el sufijo al nombre del archivo.

    Retorna una tupla: (content_disposition_header_value, clean_full_filename)
    """
    safe_base = sanitize_filename(filename_base)
    ext = extension.lstrip(".")
    full_name = f"{safe_base}.{ext}"

    disposition = f'attachment; filename="{full_name}"'
    return disposition, full_name
