/**
 * login-page.js
 * Funcionalidad mejorada para la página de login
 */

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initLoginPage();
});

/**
 * Inicializar la página de login
 */
function initLoginPage() {
    // Inicializar iconos de Feather
    if (typeof feather !== 'undefined') {
        feather.replace();
    }

    // Event listener para toggle de contraseña
    const togglePasswordBtn = document.getElementById('togglePassword');
    if (togglePasswordBtn) {
        togglePasswordBtn.addEventListener('click', togglePasswordVisibility);
    }

    // Event listener para el formulario
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginSubmit);
    }

    // Auto-focus en el campo de documento
    const documentoInput = document.getElementById('documento');
    if (documentoInput) {
        documentoInput.focus();
    }

    // Limpiar error al escribir
    const inputs = document.querySelectorAll('.form-control-modern');
    inputs.forEach(input => {
        input.addEventListener('input', hideErrorMessage);
    });
}

/**
 * Toggle para mostrar/ocultar contraseña
 */
function togglePasswordVisibility() {
    const passwordInput = document.getElementById('pass');
    const eyeIcon = document.getElementById('eyeIcon');

    if (!passwordInput || !eyeIcon) return;

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.setAttribute('data-feather', 'eye-off');
    } else {
        passwordInput.type = 'password';
        eyeIcon.setAttribute('data-feather', 'eye');
    }

    // Reinicializar iconos de Feather
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

/**
 * Manejar el envío del formulario
 */
function handleLoginSubmit(event) {
    event.preventDefault();

    const documento = document.getElementById('documento');
    const password = document.getElementById('pass');
    const btnLogin = document.getElementById('btn_login');

    // Validar campos
    if (!documento || !password) {
        showErrorMessage('Error: Campos no encontrados');
        return;
    }

    if (!documento.value || !password.value) {
        showErrorMessage('Por favor complete todos los campos');
        return;
    }

    // Validar documento (debe ser numérico)
    if (isNaN(documento.value) || documento.value.length < 5) {
        showErrorMessage('Por favor ingrese un número de documento válido');
        return;
    }

    // Validar contraseña (mínimo 4 caracteres)
    if (password.value.length < 4) {
        showErrorMessage('La contraseña debe tener al menos 4 caracteres');
        return;
    }

    // Deshabilitar botón y mostrar loading
    if (btnLogin) {
        btnLogin.disabled = true;
        btnLogin.classList.add('loading');
    }

    // Ocultar errores previos
    hideErrorMessage();

    // El login real se maneja en loggin.js
    // Este código solo mejora la UX
}

/**
 * Mostrar mensaje de error
 */
function showErrorMessage(message) {
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    const btnLogin = document.getElementById('btn_login');

    if (errorMessage && errorText) {
        errorText.textContent = message;
        errorMessage.classList.add('show');

        // Ocultar después de 7 segundos
        setTimeout(() => {
            hideErrorMessage();
        }, 4000);
    }

    // Habilitar botón
    if (btnLogin) {
        btnLogin.disabled = false;
        btnLogin.classList.remove('loading');
    }

    // Reinicializar iconos de Feather
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

/**
 * Ocultar mensaje de error
 */
function hideErrorMessage() {
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        errorMessage.classList.remove('show');
    }
}

/**
 * Mostrar loader general
 */
function showLoader() {
    const loader = document.querySelector('.loader-wrapper');
    if (loader) {
        loader.classList.add('active');
    }
}

/**
 * Ocultar loader general
 */
function hideLoader() {
    const loader = document.querySelector('.loader-wrapper');
    if (loader) {
        loader.classList.remove('active');
    }
}

// Exponer funciones globalmente para que loggin.js pueda usarlas
window.showLoginError = showErrorMessage;
window.hideLoginError = hideErrorMessage;
window.showLoginLoader = showLoader;
window.hideLoginLoader = hideLoader;
