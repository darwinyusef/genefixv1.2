const user = localStorage.getItem('user');



if (!user) {
    // No existe usuario -> Redireccionar al login
    location.href = 'index.html';
}

const userjson = JSON.parse(user);
if (userjson['rol'] !== 'admin') {
    document.getElementById('rol_user').remove();

} else {
    document.getElementById('rol_admin').remove();
}
document.querySelector('.user-desc').textContent = userjson['rol'];
document.querySelector('.user-name').textContent = userjson['user'];


function logout() {
    localStorage.removeItem('user'); // Eliminar el usuario del localStorage
    location.href = 'index.html';    // Redireccionar al login
}