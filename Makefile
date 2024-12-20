.PHONY: build up down main test  logs shell clean rebuild restart help

# Service name principal in docker-compose.yml
SERVICE=app

# Command base for docker-compose
COMPOSE=docker-compose

# Command for running tests
TEST_CMD=pytest --disable-warnings

help:
	@echo "Usage:"
	@echo "  make build        - Build Docker images"
	@echo "  make up           - Start all containers in the background"
	@echo "  make down         - Stop and remove containers"
	@echo "  make main         - Run the main application"
	@echo "  make test         - Run tests inside the Docker container"
	@echo "  make logs         - Show logs of the running application"
	@echo "  make shell        - Access the shell of the app container"
	@echo "  make clean        - Clean up unused Docker resources"
	@echo "  make rebuild      - Stop, remove, build, and restart all containers"
	@echo "  make restart      - Restart all containers"

build:
	@$(COMPOSE) build

up:
	@$(COMPOSE) up -d

down:
	@$(COMPOSE) down

main:
	@$(COMPOSE) run --rm $(SERVICE) sh -c "python main.py"

test:
	@$(COMPOSE) run --rm $(SERVICE) sh -c "$(TEST_CMD)"


logs:
	@$(COMPOSE) logs -f $(SERVICE)

shell:
	@$(COMPOSE) exec $(SERVICE) sh

clean:
	@docker system prune -f
	@docker volume prune -f

rebuild: down clean build up

restart: down up
