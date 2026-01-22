from qdrant_client import QdrantClient
from qdrant_client.http import models
from backend.config import settings

class QdrantHandler:
    def __init__(self):
        # If QDRANT_URL is set (from env), use it. e.g. "http://localhost:6333" for Docker
        # If not set (None), use path based storage (Embedded)
        if settings.QDRANT_URL:
            print(f"Connecting to Qdrant at {settings.QDRANT_URL}")
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
        else:
            print(f"Using Embedded Qdrant at {settings.QDRANT_PATH}")
            self.client = QdrantClient(path=settings.QDRANT_PATH)
            
        self.collection_name = settings.COLLECTION_NAME

    def ensure_collection_exists(self):
        """
        Checks if the collection exists, and if not, creates it.
        We use Cosine distance for semantic similarity.
        """
        collections = self.client.get_collections()
        exists = any(c.name == self.collection_name for c in collections.collections)

        if not exists:
            print(f"Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Size for all-MiniLM-L6-v2
                    distance=models.Distance.COSINE
                )
            )
        else:
            print(f"Collection {self.collection_name} already exists.")

    def upsert_points(self, points: list[models.PointStruct]):
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, vector: list[float], limit: int = 5, filter_conditions: dict = None):
        query_filter = None
        if filter_conditions:
            must_conditions = []
            for key, value in filter_conditions.items():
                if value is not None:
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )
            if must_conditions:
                query_filter = models.Filter(must=must_conditions)

        return self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit,
            query_filter=query_filter
        ).points

# Global instance
db_client = QdrantHandler()
