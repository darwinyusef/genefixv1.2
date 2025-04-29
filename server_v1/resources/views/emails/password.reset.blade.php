<x-mail::message>
    # Restablecer su Contraseña

    Ha solicitado restablecer su contraseña. Por favor, haga clic en el siguiente botón para continuar:

    <x-mail::button :url="$resetUrl">
        Restablecer Contraseña
    </x-mail::button>

    Si no solicitó este restablecimiento de contraseña, puede ignorar este correo electrónico.

    Gracias,
    {{ config('app.name') }}
</x-mail::message>
