.PHONY: help build up down restart logs clean backup restore

# Variables
BACKUP_DIR := ./backups
DATE := $(shell date +%Y%m%d_%H%M%S)

# Colores para output
GREEN := \033[0;32m
NC := \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "GeneFIX - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  ${GREEN}%-20s${NC} %s\n", $$1, $$2}'

setup: ## Configuración inicial (copiar .env.example a .env)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "${GREEN}✓${NC} Archivo .env creado. Por favor, edítalo con tus valores."; \
	else \
		echo "${GREEN}✓${NC} El archivo .env ya existe."; \
	fi

build: ## Construir las imágenes Docker
	@echo "${GREEN}Construyendo imágenes Docker...${NC}"
	docker-compose build

up: ## Iniciar los servicios
	@echo "${GREEN}Iniciando servicios...${NC}"
	docker-compose up -d
	@echo "${GREEN}✓${NC} Servicios iniciados"
	@echo "Frontend: http://localhost"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/genefix-dc"

down: ## Detener los servicios
	@echo "${GREEN}Deteniendo servicios...${NC}"
	docker-compose down
	@echo "${GREEN}✓${NC} Servicios detenidos"

restart: down up ## Reiniciar los servicios

logs: ## Ver logs de todos los servicios
	docker-compose logs -f

logs-backend: ## Ver logs del backend
	docker-compose logs -f backend

logs-frontend: ## Ver logs del frontend
	docker-compose logs -f frontend

logs-db: ## Ver logs de la base de datos
	docker-compose logs -f db

ps: ## Ver estado de los contenedores
	docker-compose ps

shell-backend: ## Abrir shell en el contenedor del backend
	docker-compose exec backend bash

shell-db: ## Abrir psql en la base de datos
	docker-compose exec db psql -U genefix -d genefix_db

migrate: ## Ejecutar migraciones de base de datos
	@echo "${GREEN}Ejecutando migraciones...${NC}"
	docker-compose exec backend alembic upgrade head
	@echo "${GREEN}✓${NC} Migraciones completadas"

migrate-create: ## Crear una nueva migración (uso: make migrate-create MSG="descripcion")
	@if [ -z "$(MSG)" ]; then \
		echo "Error: Especifica un mensaje con MSG=\"tu mensaje\""; \
		exit 1; \
	fi
	docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

backup: ## Crear backup de la base de datos
	@echo "${GREEN}Creando backup...${NC}"
	@mkdir -p $(BACKUP_DIR)
	@docker-compose exec -T db pg_dump -U genefix genefix_db | gzip > $(BACKUP_DIR)/genefix_$(DATE).sql.gz
	@echo "${GREEN}✓${NC} Backup creado: $(BACKUP_DIR)/genefix_$(DATE).sql.gz"

restore: ## Restaurar backup (uso: make restore FILE=backups/genefix_20240101_020000.sql.gz)
	@if [ -z "$(FILE)" ]; then \
		echo "Error: Especifica el archivo con FILE=ruta/al/backup.sql.gz"; \
		exit 1; \
	fi
	@if [ ! -f "$(FILE)" ]; then \
		echo "Error: El archivo $(FILE) no existe"; \
		exit 1; \
	fi
	@echo "${GREEN}Restaurando backup $(FILE)...${NC}"
	@gunzip -c $(FILE) | docker-compose exec -T db psql -U genefix -d genefix_db
	@echo "${GREEN}✓${NC} Backup restaurado"

clean: ## Limpiar contenedores, volúmenes e imágenes no usadas
	@echo "${GREEN}Limpiando recursos Docker...${NC}"
	docker-compose down -v
	docker system prune -f
	@echo "${GREEN}✓${NC} Limpieza completada"

clean-all: ## Limpiar TODO (incluyendo volúmenes de datos)
	@echo "${GREEN}¿ADVERTENCIA: Esto eliminará TODOS los datos de la base de datos. Continuar? [y/N]${NC}" && read ans && [ $${ans:-N} = y ]
	docker-compose down -v
	docker system prune -af --volumes
	@echo "${GREEN}✓${NC} Todo limpiado"

rebuild: down build up ## Reconstruir e iniciar los servicios

stats: ## Ver uso de recursos de los contenedores
	docker stats

healthcheck: ## Verificar salud de los servicios
	@echo "${GREEN}Verificando servicios...${NC}"
	@echo "\nBackend:"
	@curl -s http://localhost:8000/ || echo "❌ Backend no responde"
	@echo "\n\nFrontend:"
	@curl -s -o /dev/null -w "%{http_code}" http://localhost/ || echo "❌ Frontend no responde"
	@echo "\n\nBase de datos:"
	@docker-compose exec -T db pg_isready -U genefix || echo "❌ Base de datos no responde"
	@echo ""

install-docker: ## Instalar Docker y Docker Compose en Ubuntu
	@echo "${GREEN}Instalando Docker...${NC}"
	sudo apt update
	sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	echo "deb [arch=$$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt update
	sudo apt install -y docker-ce docker-ce-cli containerd.io
	sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$$(uname -s)-$$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	@echo "${GREEN}✓${NC} Docker instalado. Agrega tu usuario al grupo docker con:"
	@echo "  sudo usermod -aG docker $$USER"
	@echo "  newgrp docker"
