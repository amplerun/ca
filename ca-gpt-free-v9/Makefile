.PHONY: all setup dev build up down logs test clean install-tools

# ==============================================================================
# VARIABLES
# ==============================================================================
DOCKER_COMPOSE_FILE := .devcontainer/docker-compose.yml
DOCKER_COMPOSE := docker compose -f $(DOCKER_COMPOSE_FILE)

# ==============================================================================
# MAIN TARGETS
# ==============================================================================

# Default target
all: help

# Setup the entire development environment from scratch
setup: clean install-tools
	@echo ">> Setting up services..."
	$(DOCKER_COMPOSE) build --no-cache
	$(DOCKER_COMPOSE) up -d --remove-orphans
	@echo ">> Running initial setup script inside dev container..."
	docker exec -it ca-gpt-free-v9-dev-container /bin/bash /workspace/ca-gpt-free-v9/.devcontainer/init.sh
	@echo "✅ Full setup complete. Environment is ready."
	@echo "Run 'make dev' to attach to services and view logs."

# Run all services in development mode with logs
dev:
	@echo ">> Starting services in development mode..."
	$(DOCKER_COMPOSE) up -d
	@echo ">> Attaching to logs. Press Ctrl+C to stop."
	$(DOCKER_COMPOSE) logs -f

# Build all Docker images
build:
	@echo ">> Building all Docker images..."
	$(DOCKER_COMPOSE) build

# Start all services in the background
up:
	@echo ">> Starting all services in detached mode..."
	$(DOCKER_COMPOSE) up -d

# Stop and remove all services
down:
	@echo ">> Stopping and removing all services..."
	$(DOCKER_COMPOSE) down -v --remove-orphans

# Show logs for all services
logs:
	@echo ">> Tailing logs for all services..."
	$(DOCKER_COMPOSE) logs -f

# Run all tests across the monorepo
test:
	@echo ">> Running server tests..."
	$(DOCKER_COMPOSE) exec -T server npm test
	@echo "\n>> Running engine tests..."
	$(DOCKER_COMPOSE) exec -T engine poetry run pytest
	@echo "\n>> Running AI service tests..."
	$(DOCKER_COMPOSE) exec -T ai-service poetry run pytest
	@echo "\n✅ All tests completed."

# Run database migrations
migrate:
	@echo ">> Running database migrations..."
	$(DOCKER_COMPOSE) exec -T server npm run migrate

# Clean up Docker resources
clean: down
	@echo ">> Pruning Docker system..."
	docker system prune -af --volumes

# ==============================================================================
# HELP
# ==============================================================================
help:
	@echo "--------------------------------------------------------"
	@echo " ca-gpt-free-v9 Development Makefile"
	@echo "--------------------------------------------------------"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Core Targets:"
	@echo "  setup         - Run this once. Cleans, builds, starts, and seeds the DB."
	@echo "  dev           - Starts services and tails logs for active development."
	@echo ""
	@echo "Lifecycle:"
	@echo "  up            - Start all services in the background."
	@echo "  down          - Stop and remove all services and volumes."
	@echo "  build         - Build (or rebuild) all docker images."
	@echo "  clean         - Stop services and prune all Docker data (images, volumes)."
	@echo ""
	@echo "Development:"
	@echo "  logs          - Tail the logs of all running services."
	@echo "  test          - Run the test suites for all services."
	@echo "  migrate       - Run database migrations."
	@echo ""
	@echo "--------------------------------------------------------"