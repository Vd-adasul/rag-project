import chromadb
from chromadb.config import Settings

print(" Initializing AI Brain...")
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

collection = client.get_or_create_collection(
    name="techcorp_docs",
    metadata={"hnsw:space": "cosine"}
)

print(f" Brain Created: {collection.name}")
print(f" Memories: {collection.count()}")
print(" AI Brain Ready!")
