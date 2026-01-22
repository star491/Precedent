import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Qdrant Settings
    # If URL is None, it uses local disk mode (Embedded)
    QDRANT_URL = os.getenv("QDRANT_URL", None)
    QDRANT_PATH = "qdrant_local_db"
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
    
    # Collection Names
    COLLECTION_NAME = "institutional_memory"
    
    # Model Settings
    # Using Groq Llama 3.3
    LLM_MODEL = "llama-3.3-70b-versatile"
    
    # Using Local Sentence Transformer
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

settings = Config()
