import { API_URL } from "./config.js";

export async function getMediaInfo(url) {

  const response = await fetch(`${API_URL}/info`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: url })
  });

  const data = await response.json();
  return data;
}

export async function downloadVideo(url, quality, title = null) {
  const response = await fetch(`${API_URL}/download/video`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url, quality, title })
  });

  // Manejo de errores de la API (ej. 400 Bad Request o 500 Internal Error)
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'No se pudo descargar el video');
  }

  // 1. Extraer el nombre sugerido del archivo enviado por FastAPI en las cabeceras
  const contentDisposition = response.headers.get('content-disposition');
  let filename = 'video.mp4';

  if (contentDisposition) {
    const match = contentDisposition.match(/filename="?([^"]+)"?/i);

    if (match) {
      filename = match[1];
    }
  }

  // 2. Convertir la respuesta HTTP a un objeto Blob
  const blob = await response.blob();

  // 3. Retornar el objeto con la información necesaria
  return { blob, filename };
}

export async function downloadAudio(url, bitrate, title = null) {
  const response = await fetch(`${API_URL}/download/audio`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: url, bitrate: bitrate, title: title })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error al procesar el audio');
  }

  // Obtenemos el nombre del archivo (ej: "Cancion_oficial.mp3") que envía el backend
  const contentDisposition = response.headers.get('content-disposition');
  let filename = 'audio_descargado.mp3';

  if (contentDisposition && contentDisposition.includes('filename=')) {
    filename = contentDisposition.split('filename=')[1].replace(/["']/g, '');
  }

  // Convertimos la respuesta a Blob
  const blob = await response.blob();

  return { blob, filename };
}