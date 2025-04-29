function mostrarAlerta(mensaje, tipo) {
    const alerta = document.getElementById('alerta');
    alerta.textContent = mensaje;
    alerta.addClassList.remove('alert-success', 'alert-danger', 'alert-warning', 'alert-info', 'alert-primary', 'alert-secondary', 'alert-light', 'alert-dark');
    alerta.classList.add(`alert-${tipo}`); // Agregar la clase de tipo de alerta
    alerta.style.display = 'block';
    alerta.classList.add('fade-in');

    setTimeout(() => {
        alerta.classList.remove('fade-in');
        alerta.classList.add('fade-out');

        alerta.addEventListener('animationend', () => {
            alerta.style.display = 'none';
            alerta.classList.remove('fade-out');
        }, { once: true });

    }, 7000); // 7 segundos
}


// Puedes llamarlo cuando lo necesites


function obtenerFechaActual() {
    const fecha = new Date();

    const anio = fecha.getFullYear();
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const dia = String(fecha.getDate()).padStart(2, '0');
    const horas = String(fecha.getHours()).padStart(2, '0');
    const minutos = String(fecha.getMinutes()).padStart(2, '0');
    const segundos = String(fecha.getSeconds()).padStart(2, '0');

    return `${anio}-${mes}-${dia} ${horas}:${minutos}:${segundos}`;
}


document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.loader-wrapper').classList.add('d-none');
});