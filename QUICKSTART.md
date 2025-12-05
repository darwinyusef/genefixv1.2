# GeneFIX - Inicio Rápido con Docker

Guía rápida para desplegar GeneFIX en Ubuntu con Docker.

## 🚀 Despliegue en 5 minutos

### 1. Instalar Docker (si no lo tienes)

```bash
# Usando el Makefile
make install-docker

# O manualmente (ver DOCKER_DEPLOYMENT.md para detalles)
```

### 2. Configurar el proyecto

```bash
# Copiar el archivo de configuración
make setup

# O manualmente:
cp .env.example .env
```

### 3. Editar configuración

```bash
nano .env
```

**Valores mínimos requeridos:**

```bash
# Base de datos
DB_PASSWORD=tu_password_segura

# Seguridad (generar con: openssl rand -hex 32)
SECRET_KEY=tu_clave_secreta_generada

# URL del backend (cambiar para producción)
API_URL=http://localhost:8000/api/v1
# Para producción: http://TU_IP_PUBLICA:8000/api/v1

# Email (configurar Gmail App Password)
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password-16-chars
SMTP_FROM_EMAIL=tu-email@gmail.com
```

### 4. Iniciar la aplicación

```bash
# Construir e iniciar
make build
make up

# O en un solo paso:
docker-compose up -d --build
```

### 5. Verificar

```bash
# Ver estado
make ps

# Ver logs
make logs

# Verificar salud
make healthcheck
```

## 🌐 Acceder a la aplicación

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **Documentación**: http://localhost:8000/genefix-dc

## 📋 Comandos útiles

```bash
make help              # Ver todos los comandos disponibles
make logs              # Ver logs en tiempo real
make restart           # Reiniciar servicios
make backup            # Crear backup de la base de datos
make down              # Detener servicios
```

## 🔒 Gmail App Password

1. Ve a: https://myaccount.google.com/security
2. Activa verificación en 2 pasos
3. Ve a: https://myaccount.google.com/apppasswords
4. Genera contraseña para "Correo" → "GeneFIX"
5. Copia los 16 caracteres a `SMTP_PASSWORD` en `.env`

## 🌍 Despliegue en producción

Para despliegue en servidor con IP pública:

```bash
# 1. Editar .env
API_URL=http://TU_IP_PUBLICA:8000/api/v1

# 2. Configurar firewall
sudo ufw allow 80/tcp
sudo ufw allow 8000/tcp
sudo ufw enable

# 3. Iniciar
make rebuild
```

## 🆘 Problemas comunes

### Puerto en uso

```bash
# Ver qué usa el puerto
sudo lsof -i :8000

# Detener contenedores
make down
```

### Frontend no conecta al backend

```bash
# Verificar API_URL en .env
# Reconstruir frontend
docker-compose build frontend
docker-compose up -d frontend
```

### Ver logs de errores

```bash
make logs-backend
make logs-frontend
make logs-db
```

## 📚 Documentación completa

Ver `DOCKER_DEPLOYMENT.md` para:
- Configuración detallada de producción
- HTTPS con Let's Encrypt
- Backups automáticos
- Monitoreo y mantenimiento
- Solución de problemas avanzada

## 🔄 Actualizar la aplicación

```bash
# 1. Backup
make backup

# 2. Actualizar código
git pull

# 3. Reconstruir
make rebuild

# 4. Verificar
make logs
```

---

**¿Necesitas ayuda?** Ver la documentación completa en `DOCKER_DEPLOYMENT.md`
