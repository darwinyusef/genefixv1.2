#!/bin/bash
set -e

echo "Esperando a que la base de datos esté disponible..."
# Esperar a que PostgreSQL esté listo
if [ ! -z "$DATABASE_URL" ]; then
    # Extraer el host de la URL de la base de datos
    DB_HOST=$(echo $DATABASE_URL | sed -e 's/.*@\([^:]*\).*/\1/')

    # Esperar hasta 30 segundos para que la DB esté lista
    timeout 30 bash -c "until pg_isready -h $DB_HOST > /dev/null 2>&1; do sleep 1; done" || echo "Timeout esperando base de datos (continuando de todas formas)"
fi

echo "Ejecutando migraciones de Alembic..."
alembic upgrade head

echo "Iniciando servidor FastAPI..."
exec "$@"
