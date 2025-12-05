// Configuración de la URL del API
// En Docker, usa la variable de entorno. Si no está en Docker, usa localhost por defecto
const host = (window.ENV && window.ENV.API_URL !== "${API_URL}")
    ? window.ENV.API_URL
    : "http://localhost:8000/api/v1";

// URLs alternativas (para referencia):
// const host = "http://10.201.31.4/api/v1";        // Red local
// const host = "http://190.90.5.243/api/v1";       // Producción
const token = localStorage.getItem("access_token");
const user = JSON.parse(localStorage.getItem("user"));

fetch(`${host}/profile`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json' 
        }
    })
    .then((res) => res.json())
    .then((res) => {
            if(res.detail == "Token inválido") {
                // localStorage.removeItem('registrado')
                // localStorage.removeItem('user')
                // localStorage.removeItem('access_token')
                if(window.location.pathname != '/' && window.location.pathname != '/register.html') {
                    // TODO debemos mostrar un mensaje de session expirada solo en caso de pruebas
                    // alert('La session no se encuentra activa')
                    // window.location.href = "/"
                }
            } 
    })
    .catch((e) => {
        console.error(e)
    });
