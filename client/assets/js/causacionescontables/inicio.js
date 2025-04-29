// Validar el NIT al escribir 
const inputNit = document.getElementById('id_nit');

inputNit.addEventListener('input', async function () {
    const valor = this.value;

    // Validar solo si tiene 6 caracteres
    if (valor.length > 3) {
        try {
            const response = await fetch(`http://begranda.com/equilibrium2/public/api/nits?key=${API_KEY}&f-nit_1=123&eq-nit_1=${valor}`);
            const result = await response.json();
            if (result.status == "success") {
                if (result.data.length > 0) {
                    // Encontrado
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                    // console.log('NIT encontrado');

                    const data = result.data[0]?.id;
                    // console.log('ID NIT:', data);
                } else {
                    // No encontrado
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                    console.log('NIT no encontrado: Si desea ingresarlo debe comunicarse con el administrador del sistema');
                }
                // Objeto con claves dinámicas "1", "2", "3"...


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
    const valor = campo.value.trim();

    // Eliminar comentario previo si existe
    const errorPrevio = document.querySelector(`#${id} + .invalid-feedback`);
    if (errorPrevio) errorPrevio.remove();

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


function centroCostos() {
    const select = document.getElementById('extra');
    const descripcion = document.getElementById('descripcionText');

    fetch('/assets/js/centroCostos.json')
        .then((res) => res.json())
        .then((res) => {
            console.log(res);
            res.forEach(item => {
                const option = document.createElement('option');
                option.value = item.codigo;
                option.textContent = `${item.codigo} - ${item.nombre}`;
                select.appendChild(option);
            });

            select.addEventListener('change', function () {
                const seleccionado = res.find(item => item.codigo === this.value);
                descripcion.textContent = seleccionado ? seleccionado.descripcion : 'Descripción no disponible.';
            });
        })
        .catch((e) => {
            console.error('Error al cargar los centros de costos:', e);
        });
} centroCostos();


document.getElementById("btn_guardar").addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!validarConcepto()) {
        e.preventDefault(); // Evita que se envíe el formulario
    }

    const camposValidos =
        validarCampo('id_nit', 'El NIT es obligatorio', 'num') &
        validarCampo('fecha_manual', 'La fecha manual es obligatoria') &
        validarCampo('valor', 'El valor es obligatorio', 'num') &
        validarCampo('concepto', 'El concepto es obligatorio') &
        validarCampo('extra', 'El extra es obligatorio');

    if (!camposValidos) {
        console.log("Hay errores en el formulario.");
        return;
    }

    // Capturar valores solo si pasó la validación //6068094 110510	CAJAS MENORES
    const datos = {
        documents: [
            {
                id_documento: null,
                id_comprobante: 2,
                id_nit: document.getElementById("id_nit").value.trim(),
                fecha: obtenerFechaActual().trim(),
                fecha_manual: document.getElementById("fecha_manual").value.trim(),
                id_cuenta: 6068094,
                valor: document.getElementById("valor").value.trim(),
                tipo: 1,
                concepto: document.getElementById("concepto").value.trim(),
                documento_referencia: null, // aqui va la url del archivo
                token: null,
                extra: document.getElementById("extra").value.trim() // aqui van los centros de costos
            }
        ]
    };

    console.log("Datos listos para enviar:", datos);
    /*
                "id_documento": "00000004",
                "id_comprobante": 65,
                "id_nit": 1,
                "fecha": "2024-03-19 08:00:00",
                "fecha_manual": "2024-03-19",
                "id_cuenta": 6068094,
                "valor": "100",
                "tipo": 1,
                "concepto": "ABONO CUENTA TEST VENTAS MOSTRADOR",
                "documento_referencia": "000001-3",
                "token": "f55932f7d912352222457841asasas",
                "extra": "RECIBO_GENERADO_VIA_API"
                */
    mensaje = "Este es un mensaje de alerta de ejemplo.";
    mostrarAlerta(mensaje, "success");
    // await enviarDatos(datos);

})







