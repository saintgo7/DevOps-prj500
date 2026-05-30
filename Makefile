.PHONY: help install dev up down logs test typecheck lint clean

help:
	@echo "SDG Impact Cloud — common tasks"
	@echo ""
	@echo "  make install     install all node dependencies (pnpm)"
	@echo "  make up          start local infra (postgres/redis/minio/mailhog/opensearch)"
	@echo "  make down        stop local infra"
	@echo "  make dev         run all apps (turbo dev)"
	@echo "  make logs        tail docker compose logs"
	@echo "  make test        run all unit tests"
	@echo "  make typecheck   typecheck all workspaces"
	@echo "  make lint        lint all workspaces"
	@echo "  make clean       remove build artifacts"

install:
	pnpm install

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

dev:
	pnpm dev

test:
	pnpm test

typecheck:
	pnpm typecheck

lint:
	pnpm lint

clean:
	pnpm clean
