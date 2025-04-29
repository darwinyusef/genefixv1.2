url = "/register"


function validarContraseña() {
    const passInput = document.getElementById('pass');
    const passwordConfirmInput = document.getElementById('password_confirm');
    const passwordErrors = document.getElementById('passwordErrors');
    const confirmErrors = document.getElementById('confirmErrors');

    const pass = passInput.value;
    const passwordConfirm = passwordConfirmInput.value;

    let esSegura = true;
    let errores = [];

    // Reiniciar mensajes de error y estilos
    passwordErrors.style.display = 'none';
    passInput.classList.remove('input-invalid');
    confirmErrors.style.display = 'none';
    passwordConfirmInput.classList.remove('input-invalid');

    // Validar longitud mínima (opcional, pero recomendable)
    if (pass.length < 8) {
        esSegura = false;
        errores.push("Debe tener al menos 8 caracteres.");
    }

    // Validar al menos una mayúscula
    if (!/[A-Z]/.test(pass)) {
        esSegura = false;
        errores.push("Debe tener al menos una letra mayúscula.");
    }

    // Validar al menos una minúscula
    if (!/[a-z]/.test(pass)) {
        esSegura = false;
        errores.push("Debe tener al menos una letra minúscula.");
    }

    // Validar al menos un número
    if (!/[0-9]/.test(pass)) {
        esSegura = false;
        errores.push("Debe tener al menos un número.");
    }

    // Validar al menos un símbolo (caracteres no alfanuméricos)
    if (!/[^a-zA-Z0-9\s]/.test(pass)) {
        esSegura = false;
        errores.push("Debe tener al menos un símbolo (ej: !@#$%^&*).");
    }

    // Mostrar errores de seguridad si no es segura
    if (!esSegura) {
        passInput.classList.add('input-invalid');
        passwordErrors.textContent = "La contraseña no cumple con los requisitos:\n" + errores.join("\n");
        passwordErrors.style.display = 'block';
        return false; // La contraseña no es segura
    }

    // Validar si las contraseñas coinciden
    if (pass !== passwordConfirm) {
        passwordConfirmInput.classList.add('input-invalid');
        confirmErrors.style.display = 'block';
        return false; // Las contraseñas no coinciden
    }

    return true; // La contraseña es segura y coincide
}

const formulario = document.getElementById('enviarFormulario');
const registroResultadoDiv = document.getElementById('final'); 

if (formulario) {
    formulario.addEventListener('click', async function (event) {
        event.preventDefault();
        if (!validarContraseña()) {
            alert("El formulario que intenta ingresar contiene un errror Intentelo de nuevo")
            return;
        } else {
            const documento = document.getElementById('documento').value;
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const pass = document.getElementById('pass').value;
            const userData = {
                username: documento,
                name: name,
                email: email,
                password: pass
            };
            try {
                const response = await fetch(`${host}${url}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(userData)
                });

                const data = await response.json();

                if (response.ok) {                  
                    localStorage.setItem("registrado", "ok")
                    debugger; 
                    window.location.href = "index.html"; 

                } else {
                    registroResultadoDiv.textContent = 'Error al registrar: ' + data.detail; // Ajusta según tu respuesta del backend
                    registroResultadoDiv.style.color = 'red';
                }

            } catch (error) {
                registroResultadoDiv.textContent = 'Error de red: ' + error.message;
                registroResultadoDiv.style.color = 'red';
            }
        }

    });
}

// Validación en tiempo real al quitar el foco
document.getElementById('pass').addEventListener('blur', validarContraseña);
document.getElementById('password_confirm').addEventListener('blur', validarContraseña);

// Ocultar error de confirmación al escribir
document.getElementById('password_confirm').addEventListener('input', function () {
    const confirmErrors = document.getElementById('confirmErrors');
    this.classList.remove('input-invalid');
    confirmErrors.style.display = 'none';
});

document.getElementById('pass').addEventListener('input', function () {
    const passwordErrors = document.getElementById('passwordErrors');
    this.classList.remove('input-invalid');
    passwordErrors.style.display = 'none';
});