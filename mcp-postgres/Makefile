install:
	uv sync

test:
	docker-compose up -d
	uv run python src/main.py

ruff:
	uv run --extra dev ruff check src

ruff-fix:
	uv run --extra dev ruff check src --fix

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	@find . \
		-type d \
		-name "*cache*" \
		-exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv
	@echo "Clean complete!"

status: ## Show current status
	@echo "📊 Status:"
	@echo "=========="
	@echo "Working directory: $(shell pwd)"
	@echo "Python version: $(shell python3 --version 2>&1)"
	@echo "uv version: $(shell uv --version 2>&1 || echo "❌ uv not installed")"
	@echo "Virtual environment: $(shell [ -d ".venv" ] && echo "✅ venv exists" || echo "❌ missing - run 'make setup'")"
	@echo "Dependencies: $(shell [ -f pyproject.toml ] && echo "✅ pyproject.toml exists" || echo "❌ missing")"
	@echo "Server file: $(shell [ -f src/server.py ] && echo "✅ server.py exists" || echo "❌ missing")"
	@if [ -d "venv" ]; then echo "Virtual env Python: $(shell uv run python --version 2>&1)"; fi
