const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const imgSubida = document.getElementById('imagen-subida');
const inputImagen = document.getElementById('input-imagen');

inputImagen?.addEventListener('change', () => {
  const archivo = inputImagen.files[0];
  if (archivo) {
 
    if (video.srcObject) {
      video.srcObject.getTracks().forEach(track => track.stop());
      video.style.display = "none";
    }

    
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const formData = new FormData();
    formData.append('imagen', archivo);

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
        const reader = new FileReader();
        reader.onload = e => {
          imgSubida.src = e.target.result;
          imgSubida.style.display = "block";
          imgSubida.dataset.outfitId = data.outfit_id;
          reemplazarBotones();
        };
        reader.readAsDataURL(archivo);
      } else {
        alert('Error al guardar la imagen.');
      }
    })
    .catch(() => alert('Error en la conexión.'));
  }
});


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
