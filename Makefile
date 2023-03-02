# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	RED          := $(shell tput -Txterm setaf 1)
	GREEN        := $(shell tput -Txterm setaf 2)
	BLUE         := $(shell tput -Txterm setaf 6)
	ORANGE 	     := $(shell tput -Txterm setaf 3)
	RESET 		 := $(shell tput -Txterm sgr0)
else
	RED          := ""
	GREEN        := ""
	BLUE         := ""
	RESET        := ""
endif

help: ## Show this help message
	@echo "\n\n${BLUE}################################################## Bigfishgames Makefile Help. ##################################################${RESET}"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "${BLUE}############################################################################################################################${RESET}"

IMAGE_NAME=myapp

.PHONY: local
local:
	@echo "Starting local environment..."
	docker-compose -f docker-compose.local.yml down; \
	docker-compose -f docker-compose.local.yml up

.PHONY: restart-local
restart-local:
	@echo "Restarting local environment..."
	docker-compose -f docker-compose.local.yml restart web; \

.PHONY: dev
dev:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml down; \
	docker-compose -f docker-compose.dev.yml up

.PHONY: prod
prod:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.prod.yml down; \
	docker-compose -f docker-compose.prod.yml up

.PHONY: stop
down:
	@echo "Stopping containers..."
	docker-compose -f docker-compose.local.yml down; \
	docker-compose -f docker-compose.prod.yml down

.PHONY: clean
clean:
	@echo "Cleaning up unused containers and images..."
	make down; \
	docker system prune -af

.PHONY: build-local
build-local:
	@echo "Building local image..."
	docker build -t $(IMAGE_NAME):local -f Dockerfile.local .

.PHONY: build-dev
build-dev:
	@echo "Building development image..."
	docker build -t $(IMAGE_NAME):dev -f Dockerfile.dev .

.PHONY: build-prod
build-prod:
	@echo "Building production image..."
	docker build -t $(IMAGE_NAME):prod -f Dockerfile.prod .

.PHONY: deploy
deploy:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.prod.yml up --build -deploy

PHONY: test-local
test-local:
	@echo "Running pytest unit tests within Django docker local container..."
	docker-compose -f docker-compose.local.yml run web pytest

.PHONY: test-dev
test-dev:
	@echo "Running pytest unit tests within Django docker development container..."
	docker-compose -f docker-compose.dev.yml run web pytest

.PHONY: test-prod
test-prod:
	@echo "Running pytest unit tests within Django docker production container..."
	docker-compose -f docker-compose.prod.yml run web pytest

.PHONY: migrate-local
migrate-local:
	@echo "Running Django migrations within Django docker local container..."
	docker-compose -f docker-compose.local.yml run web python manage.py migrate

.PHONY: access-local
access-local:
	@echo "Accessing Django docker local container..."
	docker-compose -f docker-compose.local.yml run web bash
