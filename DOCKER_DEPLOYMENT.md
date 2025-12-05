# GeneFIX - Guía de Despliegue con Docker en Ubuntu

Esta guía te ayudará a desplegar la aplicación GeneFIX usando Docker y Docker Compose en Ubuntu.

## Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Docker en Ubuntu](#instalación-de-docker-en-ubuntu)
3. [Configuración del Proyecto](#configuración-del-proyecto)
4. [Despliegue](#despliegue)
5. [Verificación](#verificación)
6. [Comandos Útiles](#comandos-útiles)
7. [Solución de Problemas](#solución-de-problemas)
8. [Despliegue en Producción](#despliegue-en-producción)

---

## Requisitos Previos

- Ubuntu 20.04 LTS o superior
- Acceso root o sudo
- Al menos 2GB de RAM disponible
- 10GB de espacio en disco
- Conexión a Internet

---

## Instalación de Docker en Ubuntu

### 1. Actualizar el sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Instalar Docker

```bash
# Instalar paquetes requeridos
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Agregar la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar el repositorio de Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Verificar instalación
sudo docker --version
```

### 3. Instalar Docker Compose

```bash
# Descargar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Dar permisos de ejecución
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker-compose --version
```

### 4. Configurar usuario (opcional, pero recomendado)

Para ejecutar Docker sin sudo:

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Aplicar cambios (necesitas cerrar sesión y volver a entrar)
newgrp docker

# Verificar
docker ps
```

---

## Configuración del Proyecto

### 1. Clonar o subir el proyecto al servidor

```bash
# Si tienes el proyecto localmente, súbelo usando scp:
scp -r /ruta/local/genefixv1.2 usuario@servidor:/home/usuario/

# O clona desde git si está en un repositorio
git clone <url-del-repo> genefixv1.2
cd genefixv1.2
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tu editor favorito
nano .env
# o
vim .env
```

### 3. Configurar valores importantes en `.env`

```bash
# Base de datos
DB_USER=genefix
DB_PASSWORD=TU_PASSWORD_SEGURA_AQUI
DB_NAME=genefix_db

# Seguridad - IMPORTANTE: Genera una clave segura
SECRET_KEY=$(openssl rand -hex 32)

# URL del Backend (IMPORTANTE para producción)
# Si tu servidor tiene IP pública 190.90.5.243:
API_URL=http://190.90.5.243:8000/api/v1
# O si tienes un dominio:
# API_URL=https://api.tudominio.com/api/v1

# Email (Gmail)
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password-16-caracteres
SMTP_FROM_EMAIL=tu-email@gmail.com
```

#### Configurar Gmail para SMTP

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Seguridad → Verificación en dos pasos (actívala si no lo está)
3. Contraseñas de aplicaciones: https://myaccount.google.com/apppasswords
4. Genera una contraseña para "Correo" → "Otro (Genefix)"
5. Copia la contraseña de 16 caracteres en `SMTP_PASSWORD`

---

## Despliegue

### 1. Construir las imágenes

```bash
cd /ruta/a/genefixv1.2
docker-compose build
```

Esto puede tardar varios minutos la primera vez.

### 2. Iniciar los servicios

```bash
# Iniciar en modo detached (en segundo plano)
docker-compose up -d

# O iniciar y ver los logs en tiempo real
docker-compose up
```

### 3. Verificar que los contenedores están corriendo

```bash
docker-compose ps
```

Deberías ver 3 contenedores:
- `genefix_db` (PostgreSQL)
- `genefix_backend` (FastAPI)
- `genefix_frontend` (nginx)

---

## Verificación

### 1. Verificar logs

```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Seguir logs en tiempo real
docker-compose logs -f backend
```

### 2. Verificar base de datos

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U genefix -d genefix_db

# Listar tablas
\dt

# Salir
\q
```

### 3. Acceder a la aplicación

- **Frontend**: http://localhost (o http://TU_IP_SERVIDOR)
- **Backend API**: http://localhost:8000 (o http://TU_IP_SERVIDOR:8000)
- **Documentación API**: http://localhost:8000/genefix-dc

### 4. Verificar health checks

```bash
# Backend
curl http://localhost:8000/

# Frontend
curl http://localhost/
```

---

## Comandos Útiles

### Gestión de servicios

```bash
# Detener los servicios
docker-compose stop

# Iniciar los servicios
docker-compose start

# Reiniciar los servicios
docker-compose restart

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar TODO (incluyendo volúmenes)
docker-compose down -v
```

### Ver logs

```bash
# Logs de todos los servicios
docker-compose logs -f

# Logs del backend solamente
docker-compose logs -f backend

# Últimas 100 líneas
docker-compose logs --tail=100 backend
```

### Acceder a un contenedor

```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh

# Base de datos
docker-compose exec db bash
```

### Ejecutar migraciones manualmente

```bash
docker-compose exec backend alembic upgrade head
```

### Ver uso de recursos

```bash
docker stats
```

---

## Solución de Problemas

### El backend no se conecta a la base de datos

```bash
# Verificar que la DB está corriendo
docker-compose ps db

# Ver logs de la DB
docker-compose logs db

# Reiniciar solo la DB
docker-compose restart db
```

### Error "Port already in use"

```bash
# Ver qué está usando el puerto
sudo lsof -i :8000  # Para el backend
sudo lsof -i :80    # Para el frontend

# Detener el proceso o cambiar el puerto en docker-compose.yml
```

### Reconstruir imágenes después de cambios

```bash
# Reconstruir todo
docker-compose build --no-cache

# Reconstruir un servicio específico
docker-compose build --no-cache backend

# Reconstruir e iniciar
docker-compose up -d --build
```

### Limpiar espacio en disco

```bash
# Ver uso de espacio
docker system df

# Limpiar contenedores, redes e imágenes no usadas
docker system prune -a

# Limpiar volúmenes no usados
docker volume prune
```

### El frontend no puede conectarse al backend

1. Verifica que `API_URL` en `.env` sea accesible desde el navegador
2. Si estás en producción, usa la IP pública o dominio:
   ```bash
   API_URL=http://TU_IP_PUBLICA:8000/api/v1
   ```
3. Reconstruye el frontend:
   ```bash
   docker-compose build frontend
   docker-compose up -d frontend
   ```

---

## Despliegue en Producción

### 1. Seguridad del Firewall

```bash
# Permitir puertos necesarios
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp

# Habilitar firewall
sudo ufw enable
```

### 2. Usar HTTPS con Let's Encrypt

Para producción, se recomienda usar un reverse proxy con SSL. Aquí un ejemplo con nginx:

```bash
# Instalar nginx en el host
sudo apt install nginx certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

Crear archivo de configuración nginx en el host: `/etc/nginx/sites-available/genefix`

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tudominio.com www.tudominio.com;

    ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Activar sitio
sudo ln -s /etc/nginx/sites-available/genefix /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Actualizar `.env`:
```bash
API_URL=https://tudominio.com/api/v1
```

### 3. Actualizar docker-compose para producción

Cambiar en `docker-compose.yml` para no exponer puertos innecesarios:

```yaml
# Frontend - Solo accesible desde el host
frontend:
  ports:
    - "127.0.0.1:80:80"  # Solo localhost

# Backend - Solo accesible desde el host
backend:
  ports:
    - "127.0.0.1:8000:8000"  # Solo localhost

# DB - NO exponer externamente
db:
  # ports:
  #   - "5432:5432"  # Comentar esta línea
```

### 4. Backups de base de datos

```bash
# Crear script de backup
cat > backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/genefix"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

docker-compose exec -T db pg_dump -U genefix genefix_db | gzip > $BACKUP_DIR/genefix_$DATE.sql.gz

# Mantener solo los últimos 7 backups
find $BACKUP_DIR -name "genefix_*.sql.gz" -mtime +7 -delete
EOF

chmod +x backup-db.sh

# Programar backup diario con cron
crontab -e
# Agregar línea:
# 0 2 * * * /ruta/a/backup-db.sh
```

### 5. Restaurar backup

```bash
# Listar backups
ls -lh /backups/genefix/

# Restaurar un backup
gunzip -c /backups/genefix/genefix_20240101_020000.sql.gz | \
  docker-compose exec -T db psql -U genefix -d genefix_db
```

### 6. Monitoreo

```bash
# Ver recursos en tiempo real
docker stats

# Configurar restart automático (ya está en docker-compose.yml)
# restart: unless-stopped
```

---

## Actualización de la Aplicación

```bash
# 1. Hacer backup de la base de datos
./backup-db.sh

# 2. Descargar nuevos cambios
git pull origin main

# 3. Reconstruir imágenes
docker-compose build

# 4. Reiniciar servicios
docker-compose down
docker-compose up -d

# 5. Verificar logs
docker-compose logs -f
```

---

## Resumen de Puertos

| Servicio | Puerto Interno | Puerto Externo | Descripción |
|----------|---------------|----------------|-------------|
| Frontend | 80 | 80 | Interfaz web |
| Backend | 8000 | 8000 | API REST |
| PostgreSQL | 5432 | 5432* | Base de datos |

*En producción, NO exponer el puerto de PostgreSQL externamente

---

## Soporte

Para más información:
- Ver logs: `docker-compose logs -f`
- Documentación API: http://localhost:8000/genefix-dc
- Repositorio: [URL del repositorio]

---

## Licencia

[Tu licencia aquí]
