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
            "error": 405,
            "ms": "Method Not Allowed",
            "description": "El método que estás intentando usar no está permitido en esta ruta.",
        };

        // Convertir JSON a una cadena formateada y mostrarlo en la página
        document.getElementById("jsonDisplay").textContent = JSON.stringify(jsonData, null, 4);
    </script>
</body>
</html>
