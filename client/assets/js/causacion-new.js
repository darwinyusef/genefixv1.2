/**
 * causacion-new.js
 * Script para la página de creación de nuevas causaciones contables
 */

// Configurar PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initCausacionNew();
});

function initCausacionNew() {
    // Cargar causaciones en estado "entregado"
    loadCausaciones();

    // Event listener para eliminar causaciones
    document.addEventListener('click', handleDeleteCausacion);

    // Event listener para el botón de activar/enviar archivo
    const activateBtn = document.getElementById('activate');
    if (activateBtn) {
        activateBtn.addEventListener('click', (ev) => {
            ev.preventDefault();
            enviarArchivo();
        });
    }
}

/**
 * Cargar causaciones en estado "entregado"
 */
function loadCausaciones() {
    fetch(`${host}/causacionContable`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // console.log(data);
        if (data.status_code == 204) {
            const enviarBtn = document.getElementById('enviarArchivoModal');
            const primeraBtn = document.getElementById('primera');
            if (enviarBtn) enviarBtn.hidden = true;
            if (primeraBtn) primeraBtn.hidden = false;
        }

        if (data.length > 0) {
            const totalElement = document.getElementById('total');
            const total2Element = document.getElementById('total2');
            const primeraBtn = document.getElementById('primera');

            if (totalElement) totalElement.textContent = data.length;
            if (total2Element) total2Element.textContent = data.length;
            if (primeraBtn) primeraBtn.hidden = true;

            renderCausacionCards(data);
        }
    })
    .catch(error => {
        console.error('Error al obtener los datos:', error);
        mostrarAlerta(`Error al cargar las causaciones: ${error.message}. Por favor, intente nuevamente.`, "danger", 7000);
    });
}

/**
 * Renderizar tarjetas de causaciones
 */
function renderCausacionCards(data) {
    const contenedorCards = document.getElementById('contenedor-cards');
    if (!contenedorCards) return;

    contenedorCards.innerHTML = ''; // Limpiar el contenedor

    data.forEach(item => {
        const card = document.createElement('div');
        card.classList.add('col-sm-4');

        const cardBody = document.createElement('div');
        cardBody.classList.add('card', 'rcontale', 'clean');
        cardBody.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">Registro contable <strong style="text-transform: uppercase;">${item.estado} </strong></h5>
                <div class="buttons_menu">
                    <a href="causacioncontable_form.html?id=${item.id}&view=true" class="btn btn-success clearbadge" title="Ver">👁‍🗨</a>
                    <a href="causacioncontable_form.html?id=${item.id}&view=edit" class="btn btn-info clearbadge" title="Editar">✍🏻</a>
                    <button data-id="${item.id}" class="btn btn-danger clear clearbadge" title="Eliminar">❌</button>
                </div>
                <ul>
                    <li>NIT: ${item.nit}</li>
                    <li>Fecha: ${mejorarFormatoFecha(item.fecha)}</li>
                    <li>Valor: ${item.valor}</li>
                    <li class="ellipsis">Concepto: ${item.concepto}</li>
                </ul>
            </div>
        `;

        card.appendChild(cardBody);
        contenedorCards.appendChild(card);
    });
}

/**
 * Manejar eliminación de causación
 */
function handleDeleteCausacion(event) {
    if (event.target.classList.contains('btn-danger') && event.target.classList.contains('clear')) {
        const botonBorrar = event.target;
        const idParaBorrar = botonBorrar.getAttribute('data-id');

        if (!idParaBorrar) {
            mostrarAlerta("Error: No se pudo identificar el registro a eliminar.", "danger", 7000);
            return;
        }

        if (confirm(`¿Estás seguro de que quieres borrar el registro con ID: ${idParaBorrar}?`)) {
            const urlBorrar = `${host}/causacionContable/${idParaBorrar}`;

            fetch(urlBorrar, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                mostrarAlerta(`Registro con ID: ${idParaBorrar} borrado exitosamente.`, "success", 7000);
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            })
            .catch(error => {
                console.error('Error al borrar el registro:', error);
                mostrarAlerta(`Error al eliminar el registro: ${error.message}. Por favor, intente nuevamente.`, "danger", 7000);
            });
        }
    }
}

/**
 * Mostrar vista previa del archivo PDF seleccionado
 */
function mostrarVistaPrevia() {
    const input = document.getElementById("archivoInput");
    const nombreSpan = document.getElementById("nombreArchivo");
    const tamañoSpan = document.getElementById("tamañoArchivo");
    const fileInfoContainer = document.getElementById("fileInfoContainer");
    const vistaPrevia = document.getElementById("vistaPreviaArchivo");

    if (input.files && input.files[0]) {
        const archivo = input.files[0];
        const nombre = archivo.name;
        const tipo = archivo.type;
        const tamañoBytes = archivo.size;
        const tamañoTexto = tamañoBytes > 1024 * 1024
            ? (tamañoBytes / (1024 * 1024)).toFixed(2) + " MB"
            : (tamañoBytes / 1024).toFixed(2) + " KB";

        nombreSpan.textContent = nombre;
        tamañoSpan.textContent = tamañoTexto;
        fileInfoContainer.style.display = "block";

        // Validar si el archivo es un PDF
        if (tipo === "application/pdf") {
            vistaPrevia.style.display = "block";
            const reader = new FileReader();

            reader.onload = function (e) {
                const arrayBuffer = e.target.result;
                const loadingTask = pdfjsLib.getDocument(arrayBuffer);

                loadingTask.promise.then(function (pdf) {
                    pdf.getPage(1).then(function (page) {
                        const scale = 0.5;
                        const viewport = page.getViewport({ scale: scale });

                        const canvas = document.createElement("canvas");
                        const context = canvas.getContext("2d");
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;

                        const renderContext = {
                            canvasContext: context,
                            viewport: viewport
                        };
                        page.render(renderContext);

                        const container = vistaPrevia.querySelector('.border');
                        container.innerHTML = '';
                        container.appendChild(canvas);
                    });
                });
            };

            reader.readAsArrayBuffer(archivo);
            // Reinicializar iconos de Feather después de actualizar el DOM
            setTimeout(() => feather.replace(), 100);
        } else {
            vistaPrevia.style.display = "none";
            alert("Por favor, selecciona un archivo PDF.");
            clearFile();
        }
    } else {
        fileInfoContainer.style.display = "none";
        vistaPrevia.style.display = "none";
    }
}

/**
 * Limpiar archivo seleccionado
 */
function clearFile() {
    const input = document.getElementById('archivoInput');
    const fileInfoContainer = document.getElementById('fileInfoContainer');
    const vistaPrevia = document.getElementById('vistaPreviaArchivo');

    if (input) input.value = '';
    if (fileInfoContainer) fileInfoContainer.style.display = 'none';
    if (vistaPrevia) vistaPrevia.style.display = 'none';
}

/**
 * Enviar archivo al servidor
 */
function enviarArchivo() {
    const sendFile = document.getElementById("archivoInput");

    if (!sendFile || !sendFile.files || sendFile.files.length === 0) {
        mostrarAlerta("Por favor seleccione un archivo PDF antes de enviar.", "warning", 7000);
        return;
    }

    const file = sendFile.files[0];

    // Validar que sea un PDF
    if (file.type !== 'application/pdf') {
        mostrarAlerta("Solo se permiten archivos PDF. Por favor seleccione un archivo válido.", "danger", 7000);
        return;
    }

    // Validar tamaño del archivo (máximo 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        mostrarAlerta("El archivo es demasiado grande. El tamaño máximo permitido es 10MB.", "danger", 7000);
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    for (let pair of formData.entries()) {
        console.warn(pair[0], pair[1].name, pair[1].type, pair[1].size);
    }

    fetch(`${host}/activarCausacion`, {
        method: 'POST',
        body: formData,
        headers: {
            'Authorization': `Bearer ${token}`,
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // console.log(data)
        if (data.ms == 'ok') {
            mostrarAlerta("Archivo enviado exitosamente. Redirigiendo en 5 segundos...", "success", 7000);
            var modal = document.getElementById('adjuntarArchivoModal');
            if (modal) {
                var modalInstance = new bootstrap.Modal(modal);
                modalInstance.hide();
            }
            setTimeout(() => {
                window.location.href = "causacioncontable_final.html"
            }, 5000);
        } else if (data.error) {
            mostrarAlerta(`Error: ${data.error}`, "danger", 7000);
        } else {
            mostrarAlerta("Respuesta inesperada del servidor. Verifique el resultado.", "warning", 7000);
        }
    })
    .catch(error => {
        console.error('Error al enviar el archivo:', error);
        mostrarAlerta(`Error al enviar el archivo: ${error.message}. Por favor, intente nuevamente.`, 'danger', 7000);
    });
}
