from typing import List
from sentence_transformers import SentenceTransformer
from backend.qdrant_client_wrapper import db_client
from backend.models import SearchQuery, SearchResult, DecisionNode
from backend.config import settings

# Initialize model locally
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

def embed_text(text: str) -> List[float]:
    """
    Generates embedding using local SentenceTransformer model.
    """
    return embedding_model.encode(text).tolist()

def search_decisions(query: SearchQuery) -> List[SearchResult]:
    """
    Performs a semantic search on the Qdrant index.
    """
    # 1. Embed the query locally
    vector = embed_text(query.query)
    
    # 2. Build filters
    filters = {}
    if query.filter_team:
        filters["team"] = query.filter_team

    # 3. Search
    results = db_client.search(
        vector=vector,
        limit=query.limit,
        filter_conditions=filters
    )
    
    # 4. Format outputs
    formatted_results = []
    for hit in results:
        # Filter out low relevance (noise)
        if hit.score < 0.35:
            continue
            
        # Pydantic validation
        node = DecisionNode(**hit.payload)
        
        # Handle context (which might be a list from rationale validator)
        raw_context = hit.payload.get("rationale", "")
        if isinstance(raw_context, list):
            context_str = " ".join(raw_context)
        else:
            context_str = str(raw_context)

        formatted_results.append(
            SearchResult(
                score=hit.score,
                decision=node,
                context=context_str
            )
        )
        
    return formatted_results
