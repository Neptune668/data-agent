from elasticsearch import AsyncElasticsearch


class ValueEsRepository:
    def __init__(self, client: AsyncElasticsearch):
        self.client = client

