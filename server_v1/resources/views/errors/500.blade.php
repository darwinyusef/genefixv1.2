@section('title', 'Method Not Allowed')

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <pre id="jsonDisplay"></pre>

    <script>
        // Simulación de un JSON dentro del script
        const jsonData = {
            "info": "GENEFIX",
            "error": 500,
            "ms": "Internal Server Error",
            "description": "Actualmente existe un error en el servicio debe solicitar apoyo técnico a wsgestor@gmail.com.",
        };

        // Convertir JSON a una cadena formateada y mostrarlo en la página
        document.getElementById("jsonDisplay").textContent = JSON.stringify(jsonData, null, 4);
    </script>
</body>
</html>
