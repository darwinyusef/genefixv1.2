url = "/login"

if(localStorage.getItem('registrado') != null){
    //localStorage.getItem('registrado') == "ok" ? mostrarAlerta("Se ha registrado correctamente el usuario ", "success") : ""
}

document.getElementById('btn_login').addEventListener('click', async () => {
    const documento = document.getElementById('documento').value;
    const pass = document.getElementById('pass').value;

    if (!documento || !pass) {
        alert('Debes ingresar un usuario y una contraseña');
        return;
    } else {
        // Simulamos el JSON donde validamos
        try {
            const response = await fetch(`${host}${url}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "username": documento.trim(),
                    "password": pass.trim()
                })
            });

            if(response.status == 404) {
                document.querySelector('.out404').classList.remove('none'); 
                setTimeout(() => {
                    document.querySelector('.out404').classList.add('none'); 
                }, 9000)
                return
            }
            if (!response.ok) {
                // console.log(response);

                if(response.statusText == "Unauthorized") {
                    alert('Actualmente este usuario no ha sido activado y no tiene permisos de ingreso');
                    throw new Error(errorData.message || 'Error al iniciar sesión');
                }
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error al iniciar sesión');
            }
            
            const data = await response.json();
            
            localStorage.setItem('access_token', data.access_token);
            // console.log('Token guardado en localStorage:', data.access_token);
            
            // Aquí, guardamos los datos del usuario en localStorage
            localStorage.setItem('user', JSON.stringify(data.user));
            
            setTimeout(() => {
                alert('Bienvenido a la app');
                // Limpiar formulario si es necesario
                document.getElementById('documento').value = '';
                document.getElementById('pass').value = '';
                // Redireccionamos a la página principal
                location.href = './home.html';
            }, 1000);
        } catch (error) {
            console.error('Hubo un problema con el login:', error);
            alert(error.message);
        }
    }
});
