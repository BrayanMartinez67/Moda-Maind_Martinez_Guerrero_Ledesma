function obtenerGeneroDesdeURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('genero');
}

function abrirModalMedidas() {
  const genero = obtenerGeneroDesdeURL();
  const modal = document.getElementById('modal-medidas');
  const imagen = document.getElementById('imagen-genero');
  const formulario = document.getElementById('formulario-genero');

  if (!modal || !imagen || !formulario) return;

  if (genero === 'hombre') {
    imagen.style.backgroundImage = "url('/static/Assessment/image/Hombre.jpg')"; 
    formulario.innerHTML = `
      <h3>MEDIDAS - HOMBRE</h3>
      <label>Altura:<input type="number" id="altura"></label>
      <label>Ancho de Hombros:<input type="number" id="ancho_hombros"></label>
      <label>Pecho/Espalda:<input type="number" id="pecho_espalda"></label>
      <label>Cintura:<input type="number" id="cintura"></label>
      <button onclick="guardarDesdeModal()">Calcular</button>
      <div id="resultado-tipo-cuerpo" class="resultado-tipo-cuerpo" style="margin-top: 20px;"></div>
    `;
  } else {
    imagen.style.backgroundImage = "url('/static/Assessment/image/Mujer.jpg')";
    formulario.innerHTML = `
      <h3>MEDIDAS - MUJER</h3>
      <label>Ancho de Hombros:<input type="number" id="ancho_hombros"></label>
      <label>Busto:<input type="number" id="busto"></label>
      <label>Cintura:<input type="number" id="cintura"></label>
      <label>Cadera:<input type="number" id="cadera"></label>
      <button onclick="guardarDesdeModal()">Calcular</button>
      <div id="resultado-tipo-cuerpo" class="resultado-tipo-cuerpo" style="margin-top: 20px;"></div>
    `;
  }

  modal.style.display = 'flex';
}

function cerrarModal() {
  document.getElementById('modal-medidas').style.display = 'none';
}


function calcularTipoCuerpo() {
  const genero = obtenerGeneroDesdeURL();
  const hombros = parseFloat(document.getElementById('ancho_hombros')?.value);
  const cintura = parseFloat(document.getElementById('cintura')?.value);
  const cadera = parseFloat(document.getElementById('cadera')?.value);
  const busto = parseFloat(document.getElementById('busto')?.value);
  const pecho = parseFloat(document.getElementById('pecho_espalda')?.value);
  const altura = parseFloat(document.getElementById('altura')?.value);

  if (genero === 'mujer') {
    if (busto && cadera && cintura) {
      if (Math.abs(busto - cadera) < 5 && cintura < busto * 0.75) return "reloj_arena";
      else if (cadera > busto) return "triangulo_pera";
      else if (busto > cadera) return "triangulo_invertido";
      else return "rectangulo";
    }
  } else {
    if (hombros && pecho && cintura) {
      if (hombros > pecho && pecho > cintura * 1.2) return "trapecio";
      else if (hombros > cintura * 1.3 && pecho > cintura * 1.3) return "triangulo_invertido";
      else if (Math.abs(hombros - cintura) < 5 && Math.abs(pecho - cintura) < 5) return "rectangulo";
      else if (cintura > hombros) return "triangulo";
      else return "ovalado_manzana";
    }
  }

  return null;
}

function guardarDesdeModal() {
  const tipo = calcularTipoCuerpo();
  const contenedor = document.getElementById('resultado-tipo-cuerpo');
  const tiposNombres = {
    reloj_arena: "Reloj de Arena",
    triangulo_pera: "Triángulo / Pera",
    triangulo_invertido: "Triángulo Invertido",
    rectangulo: "Rectángulo",
    ovalado_manzana: "Ovalado / Manzana",
    trapecio: "Trapezoide",
    triangulo: "Triángulo"
  };

  if (tipo && contenedor) {
    const nombre = tiposNombres[tipo] || tipo;
    contenedor.innerHTML = `
      <div class="bloque-tipo-cuerpo">
        <img src="/static/Assessment/image/sparkle.png" alt="Brillo" style="height: 24px; vertical-align: middle; margin-right: 8px;">
        <strong style="font-size: 18px;">${nombre}</strong>
      </div>
    `;

   
    const select = document.getElementById('tipo_cuerpo');
    if (select) {
      select.value = tipo;
    }

  } else {
    contenedor.innerHTML = `<span style="color: #bbb;">No se pudo calcular el tipo de cuerpo.</span>`;
  }
}
