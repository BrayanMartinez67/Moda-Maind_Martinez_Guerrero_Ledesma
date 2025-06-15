function reemplazarBotones() {
  const contenedorBotones = document.getElementById('contenedor-botones');
  const notaTexto = document.getElementById('nota-texto');
  if (!contenedorBotones || !notaTexto) return;

  contenedorBotones.innerHTML = `
    <button class="midete-btn" onclick="abrirModalGenero()">Evaluar mi outfit</button>

    <div id="overlay-genero" class="overlay-genero" style="display: none;">
      <div class="modal-genero animar-modal">
        <button class="cerrar-modal" onclick="cerrarModalGenero()" aria-label="Cerrar modal">
  <svg width="24" height="24" viewBox="0 0 24 24" class="icon-close" xmlns="http://www.w3.org/2000/svg">
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
</button>
        <div class="botones-genero">
          <button class="btn-genero" onclick="redirigirEvaluacion('hombre')">Hombre</button>
          <button class="btn-genero" onclick="redirigirEvaluacion('mujer')">Mujer</button>
        </div>
      </div>
    </div>

    <button onclick="window.location.reload()">Tomar o subir otra foto</button>
  `;

  notaTexto.innerHTML = 'Evaluamos tu estilo con precisión. Descubre qué destaca y qué puedes mejorar para lograr un look ideal.';

  notaTexto.classList.remove('nota-animada'); 
  void notaTexto.offsetWidth; 
  notaTexto.classList.add('nota-animada');
}

function abrirModalGenero() {
  document.getElementById("overlay-genero").style.display = "flex";
}
function cerrarModalGenero() {
  document.getElementById("overlay-genero").style.display = "none";
}


function mostrarSeleccionGenero() {
  const modal = document.getElementById("modalGenero");
  if (modal) {
    modal.style.display = "flex";
  }
}

function redirigirEvaluacion(genero) {
  const img = document.getElementById("imagen-subida");
  const outfitId = img?.dataset.outfitId;

  if (outfitId) {
    window.location.href = `/assessment/evaluacion/${outfitId}/?genero=${genero}`;
  } else {
    alert("No se encontró el outfit. Asegúrate de haber subido una imagen.");
  }
}


window.inicio = function () {
  window.location.href = '/inicio/';
};
