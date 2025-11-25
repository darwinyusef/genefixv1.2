/**
 * password-toggle.js
 * Funcionalidad para mostrar/ocultar contraseñas
 */

/**
 * Toggle para mostrar/ocultar el campo de contraseña
 */
function togglePassword() {
    const passwordInput = document.getElementById('new-password');
    const toggleIcon = document.getElementById('toggleIcon');

    if (!passwordInput || !toggleIcon) return;

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.setAttribute('data-feather', 'eye-off');
    } else {
        passwordInput.type = 'password';
        toggleIcon.setAttribute('data-feather', 'eye');
    }

    // Reinicializar iconos de Feather
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}
