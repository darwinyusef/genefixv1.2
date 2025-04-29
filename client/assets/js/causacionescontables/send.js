const host = require('../constantes') // Cambia esto a la URL de tu API si es diferente
// Función para realizar el GET y generar las cards
function cargarDatos() {
    const url = `${host}/api/causacion-contable?page=1&per_page=10&sort=created_at&order=desc`;

    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access_token")
        }
    })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("contenedor-cards");
            let htmlContent = '';
            document.getElementById("total").innerHTML = data.total;
            document.getElementById("total2").innerHTML = data.total;
            data.data.forEach(item => {
                htmlContent += `
                            <div class="col-sm-4">
                                <div class="card rcontale">
                                    <div class="card-body">
                                        <h5 class="card-title">${item.concepto}</h5>
                                        <a href="/causacioncontable_form.html?id=${item.id}" class="btn btn-primary clearbadge">Ver más</a>
                                    </div>
                                </div>
                            </div>
                        `;
            });
            // <button class="btn btn-danger clearbadge">Borrarlo</button>
            container.innerHTML = `
            <div class="row">
                ${htmlContent}
            </div>
            `;
        })
        .catch(error => console.error("Error al cargar los datos: ", error));
}

// Llamada a la función cuando la página esté lista
document.addEventListener("DOMContentLoaded", cargarDatos);



