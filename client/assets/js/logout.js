
const user_logout = JSON.parse(localStorage.getItem('user'));

if (!user_logout) {
    // No existe usuario -> Redireccionar al login
    localStorage.removeItem('registrado')
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    localStorage.removeItem('cuentas_cache')
}

const userjson = user_logout;
if (userjson['rol'] !== 'admin') {
    document.getElementById('rol_user').remove();

} else {
    document.getElementById('rol_admin').remove();
}
document.querySelector('.user-desc').textContent = userjson['rol'];
document.querySelector('.user-name').textContent = userjson['user'];


function logout() {
    localStorage.removeItem('registrado')
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    localStorage.removeItem('cuentas_cache') // Eliminar el usuario del localStorage
    location.href = 'index.html';    // Redireccionar al login
}