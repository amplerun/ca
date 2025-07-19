.PHONY: all setup dev build up down logs test clean

# ==============================================================================
# VARIABLES
# ==============================================================================
DOCKER_COMPOSE_FILE := .devcontainer/docker-compose.yml
DOCKER_COMPOSE := docker compose -f $(DOCKER_COMPOSE_FILE)

# ==============================================================================
# MAIN TARGETS
# ==============================================================================

all: help

setup:
	@echo ">> Building all Docker images..."
	$(DOCKER_COMPOSE) build --no-cache
	@echo ">> Starting services..."
	$(DOCKER_COMPOSE) up -d --remove-orphans
	@echo ">> Running initial setup script inside dev container..."
	docker exec -it ca-gpt-free-v9-dev-container-1 /bin/bash /workspaces/$(shell basename $(CURDIR))/.devcontainer/init.sh
	@echo "✅ Full setup complete. Environment is ready."
	@echo "Run 'make dev' to attach to services and view logs."

dev:
	@echo ">> Starting services in development mode..."
	$(DOCKER_COMPOSE) up -d
	@echo ">> Attaching to logs. Press Ctrl+C to stop."
	$(DOCKER_COMPOSE) logs -f

build:
	@echo ">> Building all Docker images..."
	$(DOCKER_COMPOSE) build

up:
	@echo ">> Starting all services in detached mode..."
	$(DOCKER_COMPOSE) up -d

down:
	@echo ">> Stopping and removing all services..."
	$(DOCKER_COMPOSE) down -v --remove-orphans

logs:
	@echo ">> Tailing logs for all services..."
	$(DOCKER_COMPOSE) logs -f

test:
	@echo ">> Running server tests..."
	docker exec -T ca-gpt-free-v9-server-1 npm test
	@echo "\n>> Running engine tests..."
	docker exec -T ca-gpt-free-v9-engine-1 poetry run pytest
	@echo "\n>> Running AI service tests..."
	docker exec -T ca-gpt-free-v9-ai-service-1 poetry run pytest
	@echo "\n✅ All tests completed."

migrate:
	@echo ">> Running database migrations..."
	docker exec -T ca-gpt-free-v9-server-1 npm run migrate

clean: down
	@echo ">> Pruning Docker system..."
	docker system prune -af --volumes

help:
	@echo "--------------------------------------------------------"
	@echo " ca-gpt-free-v9 Development Makefile"
	@echo "--------------------------------------------------------"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Core Targets:"
	@echo "  setup         - Run this once. Builds, starts, and seeds the DB."
	@echo "  dev           - Starts services and tails logs for active development."
	@echo ""
	@echo "Lifecycle:"
	@echo "  up            - Start all services in the background."
	@echo "  down          - Stop and remove all services and volumes."
	@echo "  build         - Build (or rebuild) all docker images."
	@echo "  clean         - Stop services and prune all Docker data."
	@echo ""
	@echo "Development:"
	@echo "  logs          - Tail the logs of all running services."
	@echo "  test          - Run the test suites for all services."
	@echo "  migrate       - Run database migrations."
	@echo ""
	@echo "--------------------------------------------------------"
