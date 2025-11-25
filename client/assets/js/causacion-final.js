/**
 * causacion-final.js
 * Script para la página de finalización de causaciones contables
 */

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initCausacionFinal();
});

function initCausacionFinal() {
    const n = 50; // Define el número de repeticiones
    let valor = 0;

    // Cargar causaciones activadas
    loadCausacionesActivadas();

    // Event listener para botón finalizar
    document.getElementById('finalizarTodo').addEventListener('click', handleFinalizarTodo);

    // Event listener para eliminar causaciones
    document.addEventListener('click', handleDeleteCausacion);

    // Renderizar lista de cajas
    renderListaCajas();
}

/**
 * Cargar causaciones en estado "activado"
 */
function loadCausacionesActivadas() {
    fetch(`${host}/causacionContable?type=activado`, {
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
        if (data.content == 0) {
            mostrarAlerta(`Actualmente no cuenta con causaciones a finalizar. Se volverá al inicio en 7 segundos.`, "danger", 7000);
            setTimeout(() => {
                window.location.href = "causacioncontable_new.html"
            }, 7000);
            return;
        }
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
        }

        renderCausacionCards(data);
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
    contenedorCards.innerHTML = ''; // Limpiar el contenedor si ya tiene contenido

    data.forEach(item => {
        const card = document.createElement('div');
        card.classList.add('col-sm-4');

        const cardBody = document.createElement('div');
        cardBody.classList.add('card', 'rcontale', 'clean');
        cardBody.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">Registro para finalizar: <br> <strong style="text-transform: uppercase;">${item.estado} </strong></h5>
                <ul>
                    <li>NIT: ${item.nit}</li>
                    <li>Fecha: ${mejorarFormatoFecha(item.fecha)}</li>
                    <li>Valor: ${item.valor}</li>
                    <li class="ellipsis">Concepto: ${item.concepto}</li>
                </ul>
                <div class="buttons_menu">
                    <a class="clearbadge btn btn-primary " href="${item.documento_referencia}" target="_blank" title="Descargar">📄</a>
                    <a href="causacioncontable_form.html?id=${item.id}&view=true" class="btn btn-success clearbadge" title="Ver">👁‍🗨</a>
                    <a href="causacioncontable_form.html?id=${item.id}&view=edit" class="btn btn-info clearbadge" title="Editar">✍🏻</a>
                    <button data-id="${item.id}" class="btn btn-danger clear clearbadge" title="Eliminar">❌</button>
                </div>
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
 * Finalizar causaciones
 */
async function finalizar(valorSeleccionado) {
    if (!valorSeleccionado) {
        mostrarAlerta("Error: No se seleccionó ninguna caja menor.", "danger", 7000);
        return;
    }

    const codigoSeleccionado = valorSeleccionado;

    try {
        let cuentas = [];
        const cache = localStorage.getItem("cuentas_cache");

        if (cache) {
            try {
                cuentas = JSON.parse(cache);
            } catch (e) {
                console.warn("Cache corrupto, recargando...");
                mostrarAlerta("Cache de cuentas corrupto. Recargando datos...", "warning", 7000);
                localStorage.removeItem("cuentas_cache");
                cuentas = await cargarCuentasCache();
            }
        } else {
            cuentas = await cargarCuentasCache();
        }

        console.log(codigoSeleccionado);
        const existe = cuentas.find(c =>
            String(c.id) === codigoSeleccionado || String(c.cuenta) === codigoSeleccionado
        );

        // if (!existe) {
        //     mostrarAlerta(`⚠️ El id de cuenta disponible en el sistema ${codigoSeleccionado} no existe.`, "danger", 7000);
        //     throw new Error(`La caja ${codigoSeleccionado} no existe — proceso detenido.`);
        // }

        const payload = { id_cuenta: codigoSeleccionado };

        const response = await fetch(`${host}/finalizarCausacion`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();

        if (data.ms == 'ok') {
            mostrarAlerta("Causaciones finalizadas exitosamente. Redirigiendo...", "success", 7000);
            setTimeout(() => {
                window.location.href = "causacioncontable_new.html";
            }, 3000);
        } else if (data.error) {
            mostrarAlerta(`Error al finalizar: ${data.error}`, "danger", 7000);
        } else {
            mostrarAlerta("Proceso completado. Verifique el resultado.", "warning", 7000);
        }
    } catch (error) {
        console.error('Error al finalizar el proceso:', error);
        mostrarAlerta(`Error al finalizar las causaciones: ${error.message}. Por favor, intente nuevamente.`, 'danger', 7000);
    }
}

/**
 * Manejar click en botón finalizar todo
 */
function handleFinalizarTodo(ev) {
    ev.preventDefault();
    const seleccion = document.querySelector('input[name="caja"]:checked');

    if (seleccion) {
        const valorSeleccionado = seleccion.value;
        finalizar(valorSeleccionado);
    } else {
        mostrarAlerta("Por favor seleccione una caja menor antes de continuar.", "warning", 7000);
    }
}

/**
 * Renderizar lista de cajas menores
 */
function renderListaCajas() {
    const listaCajas = document.getElementById("listaCajas");

    if (!listaCajas) return;

    // Renderizamos como radio buttons
    cajas.forEach((caja, index) => {
        const div = document.createElement("div");
        div.classList.add("form-check");
        div.innerHTML = `
            <input class="form-check-input" type="radio" name="caja" id="caja${index}" value="${caja.id}">
            <label class="form-check-label" for="caja${index}">
                (${caja.codigo}) - ${caja.nombre}
            </label>
        `;
        listaCajas.appendChild(div);
    });
}
