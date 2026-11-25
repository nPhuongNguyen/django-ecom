from django.conf import settings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

class QdrantService:
    _client = None

    @classmethod
    def get_client(cls) -> QdrantClient:
        if cls._client is None:
            cls._client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                api_key=settings.QDRANT_API_KEY
            )
        return cls._client

    @classmethod
    def init_collection(cls, collection_name: str, vector_size: int):
        """Hàm khởi tạo bộ chứa (Collection) trên Qdrant nếu nó chưa tồn tại"""
        client = cls.get_client()
        if not client.collection_exists(collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )