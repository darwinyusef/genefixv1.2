# Dockerfile para el Frontend de GeneFIX (nginx)
FROM nginx:alpine

# Copiar archivos estáticos al directorio de nginx
COPY . /usr/share/nginx/html

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar script de entrada
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Exponer puerto 8001
EXPOSE 8001

# Ejecutar script de entrada y luego nginx
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
