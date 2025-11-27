# MD2Semantic

A simple ETL pipeline that extracts Markdown files from a GitHub repository, parses them into structured sections, and loads them into PostgreSQL. Designed for semantic search, RAG, and future embedding pipelines.

---

## Features

- Extract Markdown files from any public or private GitHub repository using standard HTTP requests.
- Transform Markdown into structured sections (heading + text).
- Load structured content into PostgreSQL using JSONB via SQLAlchemy.
- Ready for semantic search or embeddings pipelines.
---

## Requirements

- Docker & Docker Compose
- Python 3.11
- GitHub Personal Access Token (to increase API rate limits)

---

## Setup

1. **Clone this repository**

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. **Create .env file**

Example .env:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

GITHUB_TOKEN=<your_github_pat>
GITHUB_OWNER=github
GITHUB_REPO=awesome-copilot
GITHUB_BRANCH=main
MAX_FILES=5
LOG_LEVEL=INFO
```
## Setup & Run

3. **Build and start Docker containers, and run the ETL pipeline**

This project uses `Makefile` to simplify commands. Simply run:

```bash
make run
```

- What this does:

       - Builds Docker images for the app and PostgreSQL.

       - Starts the containers in detached mode.

       - Executes the ETL pipeline inside the app container (src/main.py).

---

## Check data in PostgreSQL

- Connect to PostgreSQL container
```
docker exec -it md2semantic-postgres psql -U postgres
```

- View the first 10 inserted Markdown files

```sql
SELECT id, file_name, source_url, created_at
FROM markdown_files
ORDER BY created_at DESC
LIMIT 10;
```


- View the first section of each file
```sql
SELECT file_name, content->0->>'heading' AS first_heading,
       content->0->>'text' AS first_text
FROM markdown_files
LIMIT 5;
```


- Count all files

```sql
SELECT COUNT(*) FROM markdown_files;
```
---

## Cleanup

To stop and remove all containers:
```
make clean
```

---

# Pending


Optional: Use PGVector extension to store embeddings for semantic search.

### 3️⃣ Vectorization: MindsDB

What it is: MindsDB is a machine learning layer for databases. It allows you to:

Generate embeddings from text.

Perform AI-powered predictions and semantic searches directly inside your database.

Role in the pipeline:

Converts the Markdown text into vector embeddings (numerical representations of text meaning).

Stores embeddings in the database for efficient semantic search (finding the closest match to a user query).

Why use it:

You don’t need a separate ML infrastructure.

Works natively with PostgreSQL.

Makes it easy to run queries like “find the prompt most similar to this question.”

### 4️⃣ Chatbot / Semantic Search Layer

What it is: The interface your user interacts with.

Role in the pipeline:

Converts user questions into embeddings.

Searches the database for the most relevant Markdown content using the embeddings.

Returns the matched instructions or prompts as an answer.

Implementation: Could be a custom Python app or a tool that queries MindsDB/Postgres.

### 5️⃣ Data Type Notes

Markdown files = unstructured text.

Stored in Postgres as structured records (each file is a row).

Once embeddings are created, the vectors allow semantic search, making it possible to answer questions without reading the entire repo manually.

Pipeline Summary Diagram (Text Version)
GitHub Repo (.md files)
       │
       ▼
PostgreSQL Table (structured text)
       │
       ▼
MindsDB Embeddings (vectorized content)
       │
       ▼
Chatbot / Semantic Search (user queries)


### ✅ Key Points

PostgreSQL = stores and organizes the data.

MindsDB = converts text into embeddings and enables AI-powered semantic queries.

Chatbot = uses embeddings to answer questions about your documents.