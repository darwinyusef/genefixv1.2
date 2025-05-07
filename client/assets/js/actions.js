function mostrarAlerta(mensaje, tipo) {
    const alerta = document.getElementById('alerta');
    alerta.textContent = mensaje;
    alerta.style.display = "block";
    alerta.classList.add(`alert-${tipo}`); // Agregar la clase de tipo de alerta
    alerta.classList.add('fade-in');

    setTimeout(() => {
        alerta.classList.remove('fade-in');
        alerta.classList.add('fade-out');
        alerta.addClassList.remove('alert-success', 'alert-danger', 'alert-warning', 'alert-info', 'alert-primary', 'alert-secondary', 'alert-light', 'alert-dark');
        alerta.addEventListener('animationend', () => {
            alerta.style.display = 'none';
            alerta.classList.remove('fade-out');
        }, { once: true });

    }, 7000); // 7 segundos
}


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
    const loadWrapper = document.querySelector('.loader-wrapper')
    if (loadWrapper) {
        loadWrapper.classList.add('d-none');
    }
});

function mejorarFormatoFecha(fechaISO) {
    const fecha = new Date(fechaISO);

    const dia = fecha.getDate().toString().padStart(2, '0');
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0'); // Los meses en JavaScript van de 0 a 11
    const anio = fecha.getFullYear();
    const horas = fecha.getHours().toString().padStart(2, '0');
    const minutos = fecha.getMinutes().toString().padStart(2, '0');

    return `${dia}/${mes}/${anio}`;
}

function activationROl(item, navbar) {
    if (item.type === 'caption') {
        const li = document.createElement('li');
        li.classList.add('pc-item', 'pc-caption');
        const label = document.createElement('label');
        label.textContent = item.label;
        li.appendChild(label);
        navbar.appendChild(li);
    }

    if (item.type === 'item') {
        const li = document.createElement('li');
        li.classList.add('pc-item');

        const a = document.createElement('a');
        a.classList.add('pc-link');
        a.href = item.href;
        if (item.target) a.target = item.target;

        const spanIcon = document.createElement('span');
        spanIcon.classList.add('pc-micon');
        spanIcon.textContent = item.iconUrl;

        const spanText = document.createElement('span');
        spanText.classList.add('pc-mtext');
        spanText.textContent = item.text;

        a.appendChild(spanIcon);
        a.appendChild(spanText);
        li.appendChild(a);
        navbar.appendChild(li);
    }

}

fetch('assets/js/menu.json') // Cambiá la ruta si es diferente
    .then(response => response.json())
    .then(data => {

        const navbar = document.getElementById('pc-navbar');

        const us = JSON.parse(localStorage.getItem("user"));

        data.menu.forEach(item => {
            if(us.rol == "user" && item.rol == "user") {
                activationROl(item, navbar)
            } 

            if(us.rol == "admin") {
                activationROl(item, navbar)
            }

        });
    })
    .catch(error => {
        console.error('Error cargando el menú:', error);
    });



function defineTopRol() {
    const us = JSON.parse(localStorage.getItem("user"));
    document.querySelector(".pc-head-link .user-name").textContent = us.name
    document.querySelector(".pc-head-link .user-desc").textContent = us.rol == "admin" ? "Administrador" : "Usuario" 
}

defineTopRol()  