# mindsdb.Dockerfile
FROM mindsdb/mindsdb:latest

# Install RAG engine + psql handler inside MindsDB
# This ensures that the RAG model can be created and can connect to our database.
RUN pip install .[rag,postgres]
