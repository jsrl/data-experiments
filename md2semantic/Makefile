.PHONY: install test ruff ruff-fix clean run

install:
	uv sync

test:
	uv run python src/main.py

# Full pipeline: build → up → run ETL
run:
	@echo "⚙️  Building Docker images..."
	docker compose build

	@echo "🚀 Starting containers..."
	docker compose up -d

	@echo "🧠 Running ETL pipeline inside md2semantic-app..."
	docker exec md2semantic-app uv run python src/main.py

ruff:
	uv run --group dev ruff check src

ruff-fix:
	uv run --group dev ruff check src --fix

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	@find . \
		-type d \
		-name "*cache*" \
		-exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv
	@echo "Clean complete!"