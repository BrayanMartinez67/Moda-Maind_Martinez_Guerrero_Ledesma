document.addEventListener('DOMContentLoaded', () => {
  // --- Selects y tipos de cuerpo ---
  const lugarSelect = document.getElementById('lugar');
  const eventoSelect = document.getElementById('evento');
  const tipoCuerpoSelect = document.getElementById('tipo_cuerpo');
  const evaluarButton = document.getElementById('evaluarOutfitButton');

  // Llenar tipos de cuerpo según género
  const genero = getGeneroFromUrl();
  tipoCuerpoSelect.innerHTML = '<option value="" disabled selected>Selecciona un tipo de cuerpo</option>';
  (TIPOS_CUERPO[genero] || []).forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.label;
    tipoCuerpoSelect.appendChild(option);
  });
  // Llenar lugares y eventos desde el backend
  fetch('http://localhost:5000/api/lugares_eventos')
    .then(response => response.json())
    .then(lugaresEventos => {
      lugarSelect.innerHTML = '<option value="" disabled selected>Selecciona un lugar</option>';
      Object.keys(lugaresEventos).forEach(lugar => {
        const option = document.createElement('option');
        option.value = lugar;
        option.textContent = lugar.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        lugarSelect.appendChild(option);
      });

      lugarSelect.addEventListener('change', function() {
        const lugar = this.value;
        eventoSelect.innerHTML = '<option value="" disabled selected>Selecciona un evento</option>';
        (lugaresEventos[lugar] || []).forEach(ev => {
          const option = document.createElement('option');
          option.value = ev;
          option.textContent = ev.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
          eventoSelect.appendChild(option);
        });
        eventoSelect.disabled = false;
      });
    })
    .catch(error => {
      console.error('Error al cargar lugares y eventos:', error);
    });

  // Botón evaluar outfit
  if (evaluarButton) {
    evaluarButton.addEventListener('click', evaluarOutfitDesdeFormulario);
  }
});

// --- Funciones auxiliares ---

function getGeneroFromUrl() {
  const params = new URLSearchParams(window.location.search);
  let genero = params.get('genero') || '';
  if (genero === 'hombre') genero = 'hombres';
  if (genero === 'mujer') genero = 'mujeres';
  return genero;
}

function evaluarOutfitDesdeFormulario() {
  // Obtener ID de imagen desde la URL
  const pathParts = window.location.pathname.split('/');
  const imagenId = pathParts[pathParts.length - 2];
  const genero = getGeneroFromUrl();
  const lugar = document.getElementById('lugar').value;
  const evento = document.getElementById('evento').value;
  const tipo_cuerpo = document.getElementById('tipo_cuerpo').value || 'sin_tipo';

  if (!lugar || !evento || !genero) {
    alert('Por favor, completa todos los campos requeridos.');
    return;
  }
  document.getElementById('pantalla-carga').style.display = 'flex';
  fetch('http://localhost:5000/analizar-imagen-id', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      imagen_id: imagenId,
      lugar,
      evento,
      genero,
      tipo_cuerpo
    })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('pantalla-carga').style.display = 'none';
    if (!data.outfit_id && !data.id) {
      alert("No se pudo obtener el ID del outfit.");
      return;
    }
    const outfitId = data.outfit_id || data.id;
    window.location.href = `/assessment/evaluacion2/${outfitId}/?genero=${genero}`;
  })
  .catch(error => {
    document.getElementById('pantalla-carga').style.display = 'none';
    console.error('Error al evaluar el outfit:', error);
    alert('Error al evaluar el outfit: ' + error);
  });
}
function cerrarPopup() {
  document.getElementById('overlay-popup').style.display = 'none';
}

function redirigirEvaluacionDesdeEvaluacion() {
  const img = document.getElementById("imagen-subida");
  const outfitId = img?.dataset.id;
  const genero = getGeneroFromUrl();
  if (outfitId) {
    window.location.href = `/assessment/evaluacion/${outfitId}/?genero=${genero}`;
  } else {
    alert("No se encontró el outfit. Asegúrate de haber subido una imagen.");
  }
}

const TIPOS_CUERPO = {
  "hombres": [
    { value: "sin_tipo", label: "Sin tipo" },
    { value: "triangulo_invertido", label: "Triángulo invertido" },
    { value: "rectangulo", label: "Rectángulo" },
    { value: "ovalado", label: "Ovalado" },
    { value: "trapezoide", label: "Trapezoide" },
    { value: "triangulo", label: "Triángulo" }
  ],
  "mujeres": [
    { value: "sin_tipo", label: "Sin tipo" },
    { value: "reloj_arena", label: "Reloj de arena" },
    { value: "triangulo_pera", label: "Triángulo / Pera" },
    { value: "triangulo_invertido", label: "Triángulo invertido" },
    { value: "rectangulo", label: "Rectángulo" },
    { value: "ovalado_manzana", label: "Ovalado / Manzana" }
  ]
};
