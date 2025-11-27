FROM python:3.11-slim

WORKDIR /app

# Install curl for debugging/network
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first (Caching layer)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy source code
COPY src/ ./src

# Run
CMD ["uv", "run", "python", "src/main.py"]