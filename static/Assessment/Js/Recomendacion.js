document.addEventListener('DOMContentLoaded', () => {
  const lugarSelect = document.getElementById('lugar');
  const eventoSelect = document.getElementById('evento');
  lugarSelect.addEventListener('change', () => {
    eventoSelect.disabled = !lugarSelect.value;
  });
  const obtenerButton = document.getElementById('obtenerRecomendacionesButton');
  if (obtenerButton) {
    obtenerButton.addEventListener('click', obtenerRecomendacion);
  } else {
    console.error("Botón de obtener recomendaciones no encontrado.");
  }
});
function obtenerRecomendacion() {
  const lugar = document.getElementById('lugar').value;
  const evento = document.getElementById('evento').value;
  const genero = getGeneroFromUrl(); 
  const tipoCuerpo = document.getElementById('tipo_cuerpo').value || 'sin_tipo';
  if (!lugar || !evento || !genero ) {
    alert("Por favor, completa todos los campos requeridos.");
    return;
  }
  console.log('Enviando datos a la API:', { lugar, evento, genero, tipo_cuerpo: tipoCuerpo });
  fetch('http://localhost:5000/api/recomendaciones', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        lugar,
        evento,
        genero,
        tipo_cuerpo: tipoCuerpo 
    })
})
  .then(response => {
    if (!response.ok) {
      throw new Error("Error en la respuesta de la API");
    }
    return response.json();
  })
  .then(data => {
    if (!data.recomendaciones) {
      alert("No se encontraron recomendaciones.");
      return;
    }
    const recomendacion = data.recomendaciones || {};
    const parteSuperior = Array.isArray(recomendacion.tren_superior) ? recomendacion.tren_superior.join(", ") : "No disponible";
    const parteInferior = Array.isArray(recomendacion.tren_inferior) ? recomendacion.tren_inferior.join(", ") : "No disponible";
    const calzado = Array.isArray(recomendacion.calzado) ? recomendacion.calzado.join(", ") : "No disponible";
    const recomendacionDiv = document.getElementById('contenido-recomendacion');
    recomendacionDiv.innerHTML = `
      <h3>Recomendaciones:</h3>
      <p><strong>Parte superior:</strong> ${parteSuperior}</p>
      <p><strong>Parte inferior:</strong> ${parteInferior}</p>
      <p><strong>Calzado:</strong> ${calzado}</p>
    `;
    document.getElementById('overlay-popup').style.display = 'flex';
  })
  .catch(error => {
    console.error('Error al obtener las recomendaciones:', error);
    alert('Ocurrió un error al obtener las recomendaciones.');
  });
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
function getGeneroFromUrl() {
  const params = new URLSearchParams(window.location.search);
  let genero = params.get('genero') || '';
  if (genero === 'hombre') genero = 'hombres';
  if (genero === 'mujer') genero = 'mujeres';
  return genero;
}
document.addEventListener('DOMContentLoaded', () => {
  const genero = getGeneroFromUrl();
  const select = document.getElementById('tipo_cuerpo');
  select.innerHTML = '<option value="" disabled selected>Selecciona un tipo de cuerpo</option>';
  (TIPOS_CUERPO[genero] || []).forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.label;
    select.appendChild(option);
  });
});
const EVENTOS = {
  playa: ['boda', 'paseo', 'reunion_social', 'relajacion'],
  montana_bosque: ['paseo', 'reunion_social', 'relajacion'],
  campo: ['paseo', 'reunion_social', 'relajacion'],
  espacio_laboral: ['reunion', 'presentacion', 'entrevista', 'trabajo_diario'],
  
};
document.addEventListener('DOMContentLoaded', () => {
  const lugarSelect = document.getElementById('lugar');
  const eventoSelect = document.getElementById('evento');
  fetch('http://localhost:5000/api/lugares_eventos')
    .then(response => response.json())
    .then(EVENTOS => {
      lugarSelect.innerHTML = '<option value="" disabled selected>Selecciona un lugar</option>';
      Object.keys(EVENTOS).forEach(lugar => {
        const option = document.createElement('option');
        option.value = lugar;
        option.textContent = lugar.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        lugarSelect.appendChild(option);
      });
      lugarSelect.addEventListener('change', function() {
        const lugar = this.value;
        eventoSelect.innerHTML = '<option value="" disabled selected>Selecciona un evento</option>';
        if (EVENTOS[lugar]) {
          EVENTOS[lugar].forEach(ev => {
            const option = document.createElement('option');
            option.value = ev;
            option.textContent = ev.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            eventoSelect.appendChild(option);
          });
          eventoSelect.disabled = false;
        } else {
          eventoSelect.disabled = true;
        }
      });
    })
    .catch(error => {
      console.error('Error al cargar lugares y eventos:', error);
    });
});
function cerrarPopup() {
  document.getElementById('overlay-popup').style.display = 'none';
}