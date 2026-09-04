from qdrant_client import AsyncQdrantClient


class ColumnQdrantRepository:
    def __init__(self, client: AsyncQdrantClient):
        self.client = client

