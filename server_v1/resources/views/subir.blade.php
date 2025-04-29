<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Subir archivo a S3</title>
</head>

<body>
    <h1>Subir archivo a S3</h1>

    @if (session('mensaje'))
    <p style="color: green;">{{ session('mensaje') }}</p>
    @endif

    <form action="{{ route('sending.archivo') }}" method="POST" enctype="multipart/form-data">
        @csrf
        <label for="archivo">Seleccione un archivo:</label><br>
        <input type="file" name="archivo" required><br><br>

        <button type="submit">Subir a S3</button>
    </form>
</body>

</html>