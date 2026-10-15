import { getMediaInfo, downloadVideo, downloadAudio } from "./api.request.js";
document.addEventListener("DOMContentLoaded", function () {
  // Botones 
  const btnSearch = document.getElementById("search-btn");
  const spinner = btnSearch.querySelector(".spinner-border");
  const text = btnSearch.querySelector(".btn-text");

  const btnDownloadAudio = document.getElementById("download-audio-btn");
  const spinnerAudio = btnDownloadAudio.querySelector(".spinner-border");
  const textAudio = btnDownloadAudio.querySelector(".btn-text");

  const btnDownloadVideo = document.getElementById("download-video-btn");
  const spinnerVideo = btnDownloadVideo.querySelector(".spinner-border");
  const textVideo = btnDownloadVideo.querySelector(".btn-text");

  // Elementos 
  const urlInput = document.getElementById("url-input");
  const errorMessage = document.getElementById("error-message");
  const resultContainer = document.getElementById("result");
  const imageElement = document.getElementById("media-image");  
  const titleElement = document.getElementById("media-title");
  const audioQualitySelect = document.getElementById("audio-quality");
  const videoQualitySelect = document.getElementById("video-quality");

  // Guardamos la última respuesta del backend para reutilizar el título en descargas
  let currentMediaInfo = null;

  function displayMediaInfo(data) {
    // Limpiamos todos los elementos antes de mostrar la nueva información
    audioQualitySelect.innerHTML = "";
    videoQualitySelect.innerHTML = "";
    titleElement.textContent = "";
    imageElement.src = "";

    if (data) {
      currentMediaInfo = data;
      titleElement.textContent = data.title + " - " + data.duration_formatted;
      imageElement.src = data.thumbnail;

      data.video_qualities.map( resolution => {
        const option = document.createElement("option");
        option.value = resolution.height;
        option.textContent = `${resolution.resolution} ${resolution.ext} ${resolution.filesize_mb ? " - " + resolution.filesize_mb + " MB" : ""}`;
        videoQualitySelect.appendChild(option);
      })

      data.audio_options.map( bitrate => {
        const option = document.createElement("option");
        option.value = bitrate.bitrate;
        option.textContent = bitrate.label;
        audioQualitySelect.appendChild(option);
      });

    }
  }

  btnSearch.addEventListener("click", async () => {

    if (!urlInput.value) {
      errorMessage.textContent = "Por favor, ingrese una URL.";
      return;
    }

    errorMessage.textContent = "";

    spinner.classList.remove("d-none");
    text.textContent = "Buscando...";
    btnSearch.disabled = true;

    try {
      const response = await getMediaInfo(urlInput.value);

      // Solo mostramos el div si estaba oculto; nunca lo volvemos a ocultar
      resultContainer.classList.remove("d-none");

      displayMediaInfo(response);
      console.log(response);


    } catch (error) {
      console.error(error);
      errorMessage.textContent = "Ocurrió un error al realizar la búsqueda.";

    } finally {
      spinner.classList.add("d-none");
      text.textContent = "Buscar";
      btnSearch.disabled = false;
    }

  })
  

  btnDownloadVideo.addEventListener("click", async (event) => {
    
    event.preventDefault();

    spinnerVideo.classList.remove("d-none");
    textVideo.textContent = "Descargando...";
    btnDownloadVideo.disabled = true;


    try {
      
    // 1. Llamamos a la API que retorna { blob, filename }
    const title = currentMediaInfo ? currentMediaInfo.title : null;
    const { blob, filename } = await downloadVideo(urlInput.value, videoQualitySelect.value, title);
    // 2. Creamos una URL temporal en la memoria del navegador
    const downloadUrl = window.URL.createObjectURL(blob);

    // 3. Creamos una etiqueta <a> invisible, le asignamos el archivo y simulamos un clic
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = filename; // Define el nombre con el que se guardará en la carpeta Descargas
    document.body.appendChild(a);

    a.click();


    // 4. Limpieza de memoria
    a.remove();
    window.URL.revokeObjectURL(downloadUrl);

    } catch (error) {
      alert(`Ocurrió un error: ${error.message}`);
    } finally {
      spinnerVideo.classList.add("d-none");
      textVideo.textContent = "Descargar";
      btnDownloadVideo.disabled = false;
    }
  })

  btnDownloadAudio.addEventListener("click", async (event) => {
    event.preventDefault();

    spinnerAudio.classList.remove("d-none");
    textAudio.textContent = "Descargando...";
    btnDownloadAudio.disabled = true;
     try {
      // 1. Llamamos a la API que retorna { blob, filename }
      const title = currentMediaInfo ? currentMediaInfo.title : null;
      const { blob, filename } = await downloadAudio(urlInput.value, audioQualitySelect.value, title);
      // 2. Creamos una URL temporal en la memoria del navegador
      const downloadUrl = window.URL.createObjectURL(blob);

      // 3. Creamos una etiqueta <a> invisible, le asignamos el archivo y simulamos un clic
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = filename; // Define el nombre con el que se guardará en la carpeta Descargas
      document.body.appendChild(a);

      a.click();


      // 4. Limpieza de memoria
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      alert(`Ocurrió un error: ${error.message}`);
    } finally {
      spinnerAudio.classList.add("d-none");
      textAudio.textContent = "Descargar";
      btnDownloadAudio.disabled = false;
    }
  })
    
});