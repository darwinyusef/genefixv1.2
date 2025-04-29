const enviarDatos = async (datos) => {
    const formData = new FormData();
    formData.append('documents', JSON.stringify(datos.documents));

    /* for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }*/

    try {
        const response = await fetch(`http://begranda.com/equilibrium2/public/api/document?key=${API_KEY}`, {
            method: 'POST',
            body: formData,
        });

        if (response.ok && response.status === 200) {
            const data = await response.json();
            if (data.status == "success") {
                console.log('Respuesta del servidor:', data.data);
            } else {
                console.error('Error en la respuesta del servidor');
            }
        } else {
            console.error('Error en la petición');
        }
    } catch (error) {
        console.error('Error:', error);
    }
};
