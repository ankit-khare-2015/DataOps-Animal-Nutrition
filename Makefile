# Makefile for managing Airflow + Docker

.PHONY: help up down restart logs init user bash clean prune rebuild

help: ## Show this help message.
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services with Docker Compose
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose down && docker-compose up -d

logs: ## Tail logs from Docker Compose
	docker-compose logs -f

init: ## Initialize Airflow DB
	docker-compose run --rm airflow-webserver airflow db upgrade

user: ## Create Airflow admin user
	docker-compose run --rm airflow airflow users create \
		--username airflow \
		--firstname admin \
		--lastname user \
		--role Admin \
		--email admin@example.com \
		--password airflow

bash: ## Open Bash inside Airflow webserver container
	docker-compose exec airflow-webserver bash

clean: ## Remove unused Docker data
	docker system prune -f

prune: ## Remove all unused Docker images, containers, volumes
	docker system prune -a --volumes -f

rebuild: ## Rebuild all Docker images without cache
	docker-compose build --no-cache
