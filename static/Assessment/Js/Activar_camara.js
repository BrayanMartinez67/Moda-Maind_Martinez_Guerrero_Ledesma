
function activarCamara() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
      video.style.display = "block";
      imgSubida.style.display = "none";
      document.getElementById("btn-tomar-foto").style.display = "block";
      document.getElementById("btn-escanear").style.display = "none";
    })
    .catch(err => alert("Error accediendo a la cámara: " + err));
}

function tomarFotoConCuentaRegresiva() {
  const contador = document.getElementById("contador");
  let segundos = 5;
  contador.innerText = segundos;
  contador.style.display = "block";

  const intervalo = setInterval(() => {
    segundos--;
    if (segundos > 0) {
      contador.innerText = segundos;
    } else {
      clearInterval(intervalo);
      contador.style.display = "none";

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;


      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      ctx.drawImage(video, 0, 0);

      video.srcObject.getTracks().forEach(track => track.stop());
      video.style.display = "none";


      canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('imagen', blob, 'foto.jpg');

        fetch('/assessment/subir-foto/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          if (data.outfit_id) {
            
            const url = URL.createObjectURL(blob);
            const imgSubida = document.getElementById("imagen-subida");

            imgSubida.src = url;
            imgSubida.style.display = 'block';
            imgSubida.dataset.outfitId = data.outfit_id;

            reemplazarBotones(); 
          } else {
            alert('Error al guardar la imagen.');
          }
        })
        .catch(() => alert('Error en la conexión'));
      }, 'image/jpeg');
    }
  }, 1000);
}
