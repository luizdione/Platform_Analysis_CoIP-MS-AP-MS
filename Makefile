# bonder - development and operation shortcuts
.PHONY: help install test up up-gpu down dbsync baits qc lint

help:
	@echo "bonder - available targets:"
	@echo "  make install    install the package + dev deps (pip -e .[dev,web,ms])"
	@echo "  make test       run the test suite (CPU core, no GPU/R)"
	@echo "  make up         start the platform (CPU) at http://localhost:8080"
	@echo "  make up-gpu     start the platform with the NVIDIA GPU overlay"
	@echo "  make down       stop the containers"
	@echo "  make dbsync     download/verify the mouse databases (bonder db sync)"
	@echo "  make baits      validate baits and build the search FASTA"

install:
	pip install -e ".[dev,web,ms,annotate]"

test:
	python -m pytest -q

up:
	docker compose -f docker/docker-compose.yml up --build

up-gpu:
	docker compose -f docker/docker-compose.yml -f docker/docker-compose.gpu.yml up --build

down:
	docker compose -f docker/docker-compose.yml down

dbsync:
	python -m bonder.cli db sync

baits:
	python -m bonder.cli baits check
