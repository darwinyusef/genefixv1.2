// Validar el NIT al escribir 
const inputNit = document.getElementById('nit');
const API_KEY = "ybb0jhtlcug4Dhbpi6CEP7Up68LriYcPc4209786b008c6327dbe47644f133aadVlJUB0iK5VXzg0CIM8JNNHfU7EoHzU2X"


inputNit.addEventListener('input', async function () {
    const valor = this.value;

    // Validar solo si tiene 6 caracteres
    if (valor.length > 2) {
        try {
            const response = await fetch(`http://begranda.com/equilibrium2/public/api/nits?key=${API_KEY}&f-nit_1=123&eq-nit_1=${valor}`);
            const result = await response.json();
            if (result.status == "success") {
                if (result.data.length > 0) {
                    const data = result.data[0]
                    console.log(data);
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                    document.getElementById('nit_text').textContent = `Valido: ${data?.nit_1} ${data?.nombres || ''} ${data?.apellido_1 || ''}  ${data?.razon_social ? "-" + data?.razon_social : ''}`;
                    document.getElementById('id_nit').value = data?.id || '';
                } else {
                    // No encontrado
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                    console.log('NIT no encontrado: Si desea ingresarlo debe comunicarse con el administrador del sistema');
                }

            } else {
                // No encontrado
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }

        } catch (error) {
            console.error('Error en la API', error);
            this.classList.remove('is-valid');
            this.classList.add('is-invalid');
        }

    } else {
        // Si no tiene 6 caracteres, limpiar estado
        this.classList.remove('is-valid');
        this.classList.remove('is-invalid');
    }
});


// Formato de moneda para COP (Colombia)
function formatCOP(value) {
    const number = parseInt(value.replace(/\D/g, '')) || 0;
    return number.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 });
}

const valorInput = document.getElementById('valor');

valorInput.addEventListener('blur', () => {
    valorInput.value = formatCOP(valorInput.value);
});

valorInput.addEventListener('focus', () => {
    // Al enfocar, remover el formato para que sea más fácil editar
    valorInput.value = valorInput.value.replace(/\D/g, '');
});


// Función genérica para validar campos
function validarCampo(id, mensaje, tipo = 'text') {
    const campo = document.getElementById(id);
    let valor = campo.value.trim();

    console.log(id)
    let numeroEntero = 0
    // Eliminar comentario previo si existe
    const errorPrevio = document.querySelector(`#${id} + .invalid-feedback`);
    if (errorPrevio) errorPrevio.remove();
    if (id == 'valor') {
        numeroEntero = parseInt(valor.replace(/[^\d]/g, ""), 10);
        valor = parseFloat(numeroEntero).toFixed(2)
    }

    console.log(valor);
    if (valor === "" || (tipo === 'num' && isNaN(valor))) {
        campo.classList.add('is-invalid');

        const divError = document.createElement('div');
        divError.className = 'invalid-feedback';
        divError.innerText = mensaje;

        campo.after(divError);
        return false;
    } else {
        campo.classList.remove('is-invalid');
        campo.classList.add('is-valid');
        return true;
    }
}


function validarConcepto() {
    const campo = document.getElementById("concepto");
    const mensajeError = document.getElementById("conceptoError");
    const texto = campo.value.trim();
    const palabras = texto.split(/\s+/).filter(Boolean);
    const cantidadPalabras = palabras.length;

    let error = "";

    if (cantidadPalabras < 20) {
        error = "Debe tener al menos 20 palabras.";
    } else if (cantidadPalabras > 200) {
        error = "No puede tener más de 200 palabras.";
    } else if (texto === "") {
        error = "Este campo es obligatorio.";
    }

    if (error !== "") {
        campo.classList.add("is-invalid");
        mensajeError.textContent = error;
        return false;
    } else {
        campo.classList.remove("is-invalid");
        campo.classList.add("is-valid");
        mensajeError.textContent = "";
        return true;
    }
}

async function listadoCentroCostos() {
    const response = await fetch('assets/js/causacionescontables/centroCostos.json');
    const data = await response.json();

    const categoriasPrincipales = data.filter(cat => cat.descripcion === "");

    const agrupadas = {};
    categoriasPrincipales.forEach(p => {
        agrupadas[p.nombre] = [];
    });

    data.forEach(cat => {
        if (cat.descripcion && cat.tipo && agrupadas.hasOwnProperty(cat.tipo)) {
            agrupadas[cat.tipo].push(cat);
        }
    });

    const select = document.getElementById('extra');
    const descripcion = document.getElementById('descripcionText');

    for (const principal of categoriasPrincipales) {
        const optgroup = document.createElement('optgroup');
        optgroup.label = principal.nombre;

        const hijos = agrupadas[principal.nombre];
        if (hijos && hijos.length > 0) {
            hijos.forEach(hijo => {
                const option = document.createElement('option');
                option.value = hijo.codigo;
                option.textContent = `${hijo.codigo} - ${hijo.nombre}`;
                optgroup.appendChild(option);
            });
            select.appendChild(optgroup);
        }
    }
    select.addEventListener('change', function (e) {
        const seleccionado = data.find(item => item.codigo === e.target.value);
        descripcion.textContent = seleccionado ? seleccionado.descripcion : 'Descripción no disponible.';
    });


} listadoCentroCostos()

document.getElementById("btn_guardar").addEventListener("click", async (e) => {
    e.preventDefault();

    const camposValidos =
        validarCampo('nit', 'El NIT es obligatorio', 'num') &
        // validarCampo('fecha_manual', 'La fecha manual es obligatoria') &
        validarCampo('valor', 'El valor es obligatorio', 'num') &
        validarCampo('concepto', 'El concepto es obligatorio') &
        validarCampo('extra', 'El extra es obligatorio');

    if (!camposValidos) {
        console.log("Hay errores en el formulario.");
        return;
    }

    datos = levantarData()
    console.log("Datos listos para enviar:", datos);
    enviarDatos(datos);

})


document.getElementById("btn_editar").addEventListener("click", async (e) => {
    e.preventDefault();

    id_unico = document.getElementById('id_unico').value
    const camposValidos =
        validarCampo('nit', 'El NIT es obligatorio', 'num') &
        // validarCampo('fecha_manual', 'La fecha manual es obligatoria') &
        validarCampo('valor', 'El valor es obligatorio', 'num') &
        validarCampo('concepto', 'El concepto es obligatorio') &
        validarCampo('extra', 'El extra es obligatorio');

    if (!camposValidos) {
        console.log("Hay errores en el formulario.");
        return;
    }

    datos = levantarData()
    console.log("Datos listos para enviar:", datos);
    actualizarDatos(datos, id_unico);

})

function levantarData() {
    let valor = document.getElementById("valor").value.trim()
    numeroEntero = parseInt(valor.replace(/[^\d]/g, ""), 10);
    valor = parseFloat(numeroEntero).toFixed(2)

    // Capturar valores solo si pasó la validación //6068094 110510	CAJAS MENORES
    const datos = {
        id_documento: null,
        id_comprobante: 2,
        id_nit: document.getElementById("id_nit").value.trim(),
        nit: document.getElementById("nit").value.trim(),
        fecha: obtenerFechaActual().trim(),
        fecha_manual: document.getElementById("fecha_manual").value.trim(),
        id_cuenta: 6068094,
        valor: valor,
        tipo: 1,
        concepto: document.getElementById("concepto").value.trim(),
        documento_referencia: null, // aqui va la url del archivo
        token: null,
        extra: document.getElementById("extra").value.trim() // aqui van los centros de costos
    };
    return datos
}

function enviarDatos(datos) {
    fetch(`${host}/causacionContable`, {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
        .then((res) => res.json())
        .then((res) => {
            if (!res.ok) {
                mostrarAlerta("Error en la petición id: response.false", "danger");
                throw new Error("Error en la petición");
            }
            mensaje = "La causación se ha registrado correctamente.";
            mostrarAlerta(mensaje, "success");
            setTimeout(() => {
                window.location.href = "causacioncontable_new.html"
            }, 5000)
        })
        .catch((e) => {
            mostrarAlerta("Error en la petición id: " + e, "danger");
            console.log(e)
        });
}


function actualizarDatos(datos, id) {
    fetch(`${host}/causacionContable/${id}`, {
        method: "PUT",
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
        .then((res) => res.json())
        .then((res) => {
            if (!res.ok) {
                mostrarAlerta("Error en la petición id: response.false", "danger");
                throw new Error("Error en la petición");
            }
            mensaje = "La causación se ha editado correctamente.";
            mostrarAlerta(mensaje, "success");
            setTimeout(() => {
                window.location.href = "causacioncontable_new.html"
            }, 5000)
        })
        .catch((e) => {
            mostrarAlerta("Error en la petición id: " + e, "danger");
            console.log(e)
        });
}



//******************** En deprecated activo nuevamente */


const buscarCuenta = async () => {
    const cuenta = document.getElementById('f_cuenta').value;
    const nombre = document.getElementById('f_nombre').value;

    if (cuenta === "" && nombre === "") {
        alert('Por favor, ingrese un valor para buscar');
        return;
    }

    let url = `http://begranda.com/equilibrium2/public/api/account?eq-auxiliar=1&&key=${API_KEY}&`;

    if (cuenta) {
        url += `f-cuenta=${cuenta}&`;
    }

    if (nombre) {
        url += `f-nombre=${nombre}`;
    }

    try {
        const response = await fetch(url);
        const data = await response.json();
        if (data.status !== "success") {
            alert('Error al buscar cuentas contables');
            return;
        }
        mostrarResultadosCuenta(data.data);
    } catch (error) {
        console.error('Error en la búsqueda:', error);
    }
};

const mostrarResultadosCuenta = (data) => {
    const div = document.getElementById('resultadosCuenta');
    div.innerHTML = '';

    if (!data || Object.keys(data).length === 0) {
        div.innerHTML = '<p>No se encontraron resultados.</p>';
        return;
    }

    let tabla = '<table class="table table-hover">';
    tabla += '<thead><tr><th>ID</th><th>Cuenta</th><th>Nombre</th><th>Acción</th></tr></thead><tbody>';

    Object.values(data).forEach(item => {
        tabla += `
            <tr>
                <td>${item.id}</td>
                <td>${item.cuenta}</td>
                <td>${item.nombre}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="seleccionarCuenta('${item.id}', '${item.cuenta}', '${item.nombre}')">Agregar</button>
                </td>
            </tr>
        `;
    });

    tabla += '</tbody></table>';
    div.innerHTML = tabla;
};

const seleccionarCuenta = (id, cuenta, nombre) => {
    document.getElementById('id_cuenta').value = id;
    document.getElementById('inputCuentaSeleccionada').value = `${id} - ${cuenta} - ${nombre}`;
    document.getElementById('finalEnviadoCuentaSeleccionada').value = cuenta;
    finalEnviadoCuentaSeleccionada
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalBuscarCuenta'));
    modal.hide();
};






