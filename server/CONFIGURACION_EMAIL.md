# 📧 Configuración de Email para GeneFIX

Este documento explica cómo configurar el envío de emails usando Gmail para GeneFIX.

## 🔧 Configuración Rápida

### Paso 1: Habilitar Verificación en 2 Pasos en Gmail

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. En el menú lateral, haz clic en **"Seguridad"**
3. Busca **"Verificación en dos pasos"**
4. Haz clic en **"Comenzar"** y sigue los pasos para activarla

⚠️ **IMPORTANTE**: La verificación en 2 pasos es obligatoria para usar App Passwords.

### Paso 2: Generar una App Password

1. Una vez habilitada la verificación en 2 pasos, ve a:
   https://myaccount.google.com/apppasswords

2. Si no ves esta opción, busca en Google: **"Google App Passwords"**

3. Selecciona:
   - **Aplicación**: Correo
   - **Dispositivo**: Otro (nombre personalizado)
   - Escribe un nombre como: **"GeneFIX Server"**

4. Haz clic en **"Generar"**

5. Google te mostrará una contraseña de 16 caracteres (ejemplo: `abcd efgh ijkl mnop`)

6. **¡COPIA ESTA CONTRASEÑA!** No podrás verla de nuevo.

### Paso 3: Configurar Variables de Entorno

1. Copia el archivo `.env.example` y renómbralo a `.env`:
   ```bash
   cp .env.example .env
   ```

2. Abre el archivo `.env` y configura las siguientes variables:

   ```bash
   # Email Configuration
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=wsgestor@gmail.com
   SMTP_PASSWORD=abcd efgh ijkl mnop  # ⚠️ Aquí va tu App Password
   SMTP_FROM_EMAIL=wsgestor@gmail.com
   SMTP_FROM_NAME=Genefix by Yusef Gonzalez
   USE_MAILTRAP=false
   ```

3. **IMPORTANTE**:
   - Usa la App Password (16 caracteres), NO tu contraseña normal de Gmail
   - Puedes incluir o no los espacios en la App Password, ambos funcionan
   - El email en `SMTP_USERNAME` y `SMTP_FROM_EMAIL` debe ser el mismo

### Paso 4: Verificar la Configuración

Ejecuta el servidor y prueba enviar un email:

```python
from app.config.mail import enviar_email_simple

result = enviar_email_simple(
    destinatario="destinatario@ejemplo.com",
    asunto="Prueba de Email",
    mensaje="Este es un email de prueba desde GeneFIX",
    es_html=False
)
print(result)
```

Si todo está configurado correctamente, verás:
```json
{
    "success": true,
    "message": "Correo enviado exitosamente a destinatario@ejemplo.com",
    "destinatario": "destinatario@ejemplo.com"
}
```

## 🚨 Solución de Problemas

### Error: "Username and Password not accepted"

**Causa**: Credenciales incorrectas o no estás usando una App Password.

**Solución**:
1. Verifica que hayas habilitado la verificación en 2 pasos
2. Asegúrate de estar usando la **App Password**, no tu contraseña normal
3. Vuelve a generar una nueva App Password

### Error: "SMTP Authentication Error"

**Causa**: La App Password es incorrecta o ha expirado.

**Solución**:
1. Ve a https://myaccount.google.com/apppasswords
2. Revoca la App Password anterior
3. Genera una nueva App Password
4. Actualiza el archivo `.env` con la nueva contraseña

### Error: "SMTPServerDisconnected"

**Causa**: Problemas de conexión con el servidor SMTP.

**Solución**:
1. Verifica tu conexión a internet
2. Asegúrate que el puerto 587 no esté bloqueado por firewall
3. Intenta reiniciar el servidor

### Error: "Email no configurado"

**Causa**: La variable `SMTP_PASSWORD` está vacía.

**Solución**:
1. Verifica que el archivo `.env` existe
2. Verifica que `SMTP_PASSWORD` tenga un valor
3. Reinicia el servidor para cargar las variables de entorno

## 🧪 Modo Testing con Mailtrap

Si quieres probar emails sin enviarlos realmente, puedes usar Mailtrap:

1. Regístrate en https://mailtrap.io (gratis)
2. Crea un nuevo inbox
3. Obtén tu API Token y Sandbox ID
4. Configura en `.env`:
   ```bash
   USE_MAILTRAP=true
   MAILTRAP_API_TOKEN=tu_token_aqui
   MAILTRAP_SANDBOX_ID=tu_sandbox_id_aqui
   ```

Los emails se enviarán a Mailtrap en lugar de Gmail.

## 📝 Funciones Disponibles

### 1. `enviar_email_gmail()`
Envía emails usando Gmail SMTP directamente.

```python
from app.config.mail import enviar_email_gmail

result = enviar_email_gmail(
    destinatario="usuario@ejemplo.com",
    asunto="Asunto del email",
    html_body="<h1>Hola</h1><p>Este es un email HTML</p>",
    attachments=["/ruta/al/archivo.pdf"]  # Opcional
)
```

### 2. `enviar_email_simple()`
Envía emails simples (texto o HTML).

```python
from app.config.mail import enviar_email_simple

result = enviar_email_simple(
    destinatario="usuario@ejemplo.com",
    asunto="Asunto del email",
    mensaje="Este es el contenido del email",
    es_html=False  # True para HTML, False para texto plano
)
```

### 3. `enviar_correo_con_plantilla()`
Envía emails usando la plantilla HTML de GeneFIX.

```python
# Esta función se usa internamente en la API
# Ver: app/config/mail.py línea 192
```

## 🔒 Seguridad

⚠️ **NUNCA** compartas tu App Password con nadie.

⚠️ **NUNCA** subas el archivo `.env` a repositorios públicos.

✅ Mantén el archivo `.env` en `.gitignore`

✅ Usa diferentes App Passwords para diferentes aplicaciones

✅ Revoca App Passwords que ya no uses

## 📚 Referencias

- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [SMTP Settings for Gmail](https://support.google.com/a/answer/176600)
- [Python smtplib Documentation](https://docs.python.org/3/library/smtplib.html)
- [Mailtrap Documentation](https://mailtrap.io/docs/)

## 💡 Consejos Adicionales

1. **Límites de Gmail**: Gmail tiene un límite de 500 destinatarios por día para cuentas gratuitas.

2. **Logs**: Los logs de envío de email se guardan en el archivo de logs configurado. Útil para debugging.

3. **Testing**: Usa `USE_MAILTRAP=true` durante el desarrollo para no gastar tu cuota de emails de Gmail.

4. **Producción**: En producción, considera usar servicios especializados como SendGrid, Mailgun o Amazon SES para mayor confiabilidad.

---

**Última actualización**: Noviembre 2024
**Mantenido por**: Yusef Gonzalez
