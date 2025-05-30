const host = "http://localhost:8000/api/v1";
const token = localStorage.getItem("access_token");



fetch(`${host}/profile`, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json' 
        }
    })
    .then((res) => res.json())
    .then((res) => {
       
            if(res.detail == "Token inválido") {
                localStorage.removeItem('registrado')
                localStorage.removeItem('user')
                localStorage.removeItem('access_token')
                if(window.location.pathname != '/' && window.location.pathname != '/register.html') {
                    alert('La session no se encuentra activa')
                    window.location.href = "/"
                }
            } 
    })
    .catch((e) => {
        console.log(e)
    });