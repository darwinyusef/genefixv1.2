#!/bin/sh
set -e

# Reemplazar las variables de entorno en el archivo de configuración
envsubst '${API_URL}' < /usr/share/nginx/html/env-config.js > /usr/share/nginx/html/env-config.tmp.js
mv /usr/share/nginx/html/env-config.tmp.js /usr/share/nginx/html/env-config.js

# Iniciar nginx
exec "$@"
