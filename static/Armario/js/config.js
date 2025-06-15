
document.addEventListener("DOMContentLoaded", function () {
  const btn = document.querySelector(".btn-anadir");
  if (btn) {
    btn.addEventListener("click", abrirModal);
  }

  
  const fileInput = document.getElementById("id_imagen");
  const preview = document.getElementById("imagen-preview");
  const fileNameDisplay = document.getElementById("nombre-archivo");
  const label = document.getElementById("label-imagen");

  if (fileInput && preview && fileNameDisplay && label) {
    label.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", function () {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          preview.src = e.target.result;
          fileNameDisplay.textContent = file.name;
        };
        reader.readAsDataURL(file);
      } else {
        preview.src = subirImgUrl;
        fileNameDisplay.textContent = "Ningún archivo seleccionado";
      }
    });
  }

  const fileInputEditar = document.getElementById("editar-imagen");
  const fileNameDisplayEditar = document.getElementById("nombre-archivo-editar");
  const labelEditar = document.getElementById("label-editar-imagen");

  if (fileInputEditar && fileNameDisplayEditar && labelEditar) {
    labelEditar.addEventListener("click", () => fileInputEditar.click());

    fileInputEditar.addEventListener("change", function () {
      const file = fileInputEditar.files[0];
      fileNameDisplayEditar.textContent = file ? file.name : "Ningún archivo seleccionado";
    });
  }


  const tabs = document.querySelectorAll(".categoria-tab");
  const prendas = document.querySelectorAll(".prenda");

  function mostrarCategoria(nombreCategoria) {
    prendas.forEach((prenda) => {
      const cat = prenda.getAttribute("data-categoria");
      prenda.style.display = cat === nombreCategoria.toLowerCase() ? "flex" : "none";
    });
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", function (e) {
      e.preventDefault();
      tabs.forEach((t) => t.classList.remove("activo"));
      this.classList.add("activo");
      mostrarCategoria(this.getAttribute("data-categoria"));
    });
  });

  if (tabs.length > 0) {
    mostrarCategoria(tabs[0].getAttribute("data-categoria"));
  }

  const formEditar = document.getElementById("form-editar");
  if (formEditar) {
    formEditar.addEventListener("submit", function (e) {
      e.preventDefault();
      const url = formEditar.action;
      const formData = new FormData(formEditar);

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": formEditar.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: formData,
      }).then((res) => {
        if (res.ok) location.reload();
      });
    });
  }


  const formEliminar = document.getElementById("form-eliminar");
  if (formEliminar) {
    formEliminar.addEventListener("submit", function (e) {
      e.preventDefault();
      const url = formEliminar.action;

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": formEliminar.querySelector("[name=csrfmiddlewaretoken]").value,
        },
      }).then((res) => {
        if (res.ok) location.reload();
      });
    });
  }
});


function abrirModal() {
  const modal = document.getElementById('modal-prenda');
  if (!modal) return;

  modal.style.display = 'flex';

  const preview = document.getElementById("imagen-preview");
  if (preview) preview.src = subirImgUrl;

  const inputImagen = document.getElementById("id_imagen");
  if (inputImagen) inputImagen.value = "";

  const fileNameDisplay = document.getElementById("nombre-archivo");
  if (fileNameDisplay) fileNameDisplay.textContent = "Ningún archivo seleccionado";

  const categoria = document.querySelector("select[name='categoria']");
  const descripcion = document.querySelector("input[name='descripcion']");

  if (categoria && categoria.selectedIndex === 0) {
    categoria.selectedIndex = 0;
  }

  if (descripcion) {
    descripcion.value = "";
  }

  document.querySelectorAll(".error").forEach((el) => el.style.display = "none");
}

function cerrarModal() {
  const modal = document.getElementById('modal-prenda');
  if (modal) modal.style.display = 'none';
}

function abrirVisualizarModal(imagenUrl, descripcion, editarUrl, eliminarUrl, prendaId, categoriaId) {
  const modal = document.getElementById("modal-visualizar");
  const img = document.getElementById("imagen-modal");
  const desc = document.getElementById("descripcion-modal");
  const btnEditar = document.getElementById("btn-editar");
  const btnEliminar = document.getElementById("btn-eliminar");

  if (modal && img && desc && btnEditar && btnEliminar) {
    img.src = imagenUrl;
    desc.textContent = descripcion;

    btnEditar.onclick = function () {
      cerrarVisualizarModal();
      abrirModalEditar(editarUrl, descripcion, categoriaId);
    };
    btnEliminar.onclick = function () {
      cerrarVisualizarModal();
      abrirModalEliminar(eliminarUrl);
    };

    modal.style.display = "flex";
  }
}

function cerrarVisualizarModal() {
  const modal = document.getElementById("modal-visualizar");
  if (modal) modal.style.display = "none";
}

function abrirModalEditar(actionUrl, descripcion, categoriaId) {
  const form = document.getElementById("form-editar");
  if (!form) return;
  form.action = actionUrl;
  document.getElementById("editar-descripcion").value = descripcion;
  document.getElementById("editar-categoria").value = categoriaId;
  document.getElementById("modal-editar").style.display = "flex";
}

function cerrarModalEditar() {
  document.getElementById("modal-editar").style.display = "none";
}

function abrirModalEliminar(actionUrl) {
  const formEliminar = document.getElementById("form-eliminar");
  if (formEliminar) {
    formEliminar.action = actionUrl;
    document.getElementById("modal-confirmar-eliminar").style.display = "flex";
  }
}

function cerrarModalEliminar() {
  document.getElementById("modal-confirmar-eliminar").style.display = "none";
}