# GeneFIX - Despliegue del Cliente con Docker

Este documento describe cómo desplegar únicamente el **cliente (frontend)** de GeneFIX usando Docker.

## Prerrequisitos

- Docker instalado (versión 20.10 o superior)
- Docker Compose instalado (versión 2.0 o superior)
- Un servidor backend de GeneFIX ya desplegado y accesible

## Estructura de Archivos

```
.
├── client/
│   ├── Dockerfile              # Configuración de la imagen Docker del cliente
│   ├── nginx.conf              # Configuración de Nginx
│   ├── docker-entrypoint.sh    # Script de inicialización
│   ├── env-config.js           # Template de configuración de variables de entorno
│   └── ...                     # Archivos HTML, CSS, JS del cliente
├── docker-compose.yml          # Orquestación del contenedor del cliente
└── .env.example                # Ejemplo de variables de entorno
```

## Configuración

### 1. Crear archivo de variables de entorno

Copia el archivo `.env.example` y renómbralo a `.env`:

```bash
cp .env.example .env
```

### 2. Configurar variables de entorno

Edita el archivo `.env` y configura las siguientes variables:

```env
# URL del Backend API (IMPORTANTE: debe ser accesible desde el navegador del cliente)
API_URL=http://190.90.5.243/api/v1

# Puerto en el que se ejecutará el cliente (por defecto: 80)
FRONTEND_PORT=80
```

**Importante:** La variable `API_URL` debe apuntar a la URL real de tu servidor backend. Esta URL debe ser accesible desde el navegador del usuario final, **NO** desde el contenedor Docker.

Ejemplos:
- **Producción (actual):** `http://190.90.5.243/api/v1`
- **Red local:** `http://10.201.31.4/api/v1`
- **Desarrollo local:** `http://localhost:8000/api/v1`

El archivo `.env.example` ya está configurado con la URL de producción por defecto.

## Despliegue

### Opción 1: Usando Docker Compose (Recomendado)

1. **Construir y ejecutar el contenedor:**

```bash
docker-compose up -d
```

2. **Verificar que el contenedor esté corriendo:**

```bash
docker-compose ps
```

3. **Ver logs del contenedor:**

```bash
docker-compose logs -f frontend
```

4. **Acceder al cliente:**

Abre tu navegador y ve a: `http://localhost` (o el puerto que hayas configurado en `FRONTEND_PORT`)

### Opción 2: Usando Docker directamente

1. **Construir la imagen:**

```bash
docker build -t genefix-client ./client
```

2. **Ejecutar el contenedor:**

```bash
docker run -d \
  --name genefix_frontend \
  -p 80:80 \
  -e API_URL=http://localhost:8000/api/v1 \
  genefix-client
```

## Comandos Útiles

### Detener el contenedor

```bash
docker-compose down
```

### Reiniciar el contenedor

```bash
docker-compose restart
```

### Reconstruir la imagen (después de cambios en el código)

```bash
docker-compose up -d --build
```

### Ver logs en tiempo real

```bash
docker-compose logs -f frontend
```

### Entrar al contenedor (para debug)

```bash
docker exec -it genefix_frontend sh
```

## Actualizar Variables de Entorno

Si necesitas cambiar la URL del API u otras variables:

1. Edita el archivo `.env`
2. Reinicia el contenedor:

```bash
docker-compose restart frontend
```

## Solución de Problemas

### El cliente no se conecta al backend

- Verifica que `API_URL` en el archivo `.env` apunte a la URL correcta
- Asegúrate de que el backend esté corriendo y accesible
- Verifica que no haya problemas de CORS en el backend
- Abre las herramientas de desarrollo del navegador (F12) y revisa la consola

### El contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs frontend

# Verificar el estado del contenedor
docker-compose ps
```

### Puerto 80 ya está en uso

Cambia el puerto en el archivo `.env`:

```env
FRONTEND_PORT=8080
```

Luego reinicia:

```bash
docker-compose down
docker-compose up -d
```

### Problemas de permisos

En Linux, si tienes problemas de permisos con Docker:

```bash
sudo usermod -aG docker $USER
# Luego cierra sesión y vuelve a iniciar
```

## Configuración de Producción

Para producción, se recomienda:

1. **Usar un proxy reverso (Nginx/Apache) en el host:**
   - Configura SSL/TLS
   - Agrega headers de seguridad adicionales
   - Configura rate limiting

2. **Configurar el API_URL correctamente:**
   ```env
   API_URL=https://api.tudominio.com/api/v1
   ```

3. **Usar un puerto diferente si ya tienes un servidor web:**
   ```env
   FRONTEND_PORT=8080
   ```

4. **Habilitar logs persistentes:**
   ```yaml
   # En docker-compose.yml, agrega:
   volumes:
     - ./logs:/var/log/nginx
   ```

## Arquitectura

El cliente se despliega como un contenedor Docker que usa:

- **Nginx Alpine**: Servidor web ligero y eficiente
- **Variables de entorno dinámicas**: El script `docker-entrypoint.sh` reemplaza las variables de entorno en tiempo de ejecución
- **Configuración optimizada**: Compresión gzip, cache de assets estáticos, headers de seguridad

## Notas Adicionales

- El contenedor ejecuta Nginx en el puerto 80 internamente
- Los archivos estáticos se sirven desde `/usr/share/nginx/html`
- La configuración de Nginx está optimizada para aplicaciones web estáticas
- El contenedor incluye health checks para monitoreo

## Soporte

Si encuentras problemas, revisa:
1. Los logs del contenedor
2. La consola del navegador
3. Que el backend esté accesible
4. Las configuraciones de red y firewall
