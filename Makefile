IMAGE_NAME = sentiment-ai
PORT = 8080

.PHONY: build run test stop clean tag

build:
	docker build -t $(IMAGE_NAME):latest .

run:
	docker compose up -d

test:
	docker run --rm \
	-v $(PWD):/app \
	-w /app \
	$(IMAGE_NAME):latest \
	pytest tests/ -v --cov=src --cov-report=term-missing

stop:
	docker compose down

clean:
	docker compose down
	docker rmi $(IMAGE_NAME):latest || true

# Crée un tag Git annoté et le pousse vers GitHub
tag:
	@read -p "Entrez le nom du tag (ex: v1.0): " tag_name; \
	git tag -a $$tag_name -m "Release $$tag_name"; \
	git push origin $$tag_name