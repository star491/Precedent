import shutil
import os
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.qdrant_client_wrapper import db_client
from backend.ingestion import ingest_file
from backend.retrieval import search_decisions
from backend.models import SearchQuery, SearchResult

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure DB exists
    db_client.ensure_collection_exists()
    yield
    # Shutdown logic if needed

from fastapi.staticfiles import StaticFiles

# ... existing code ...

app = FastAPI(title="Precedent API", lifespan=lifespan)

# CORS (Allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for document access
STORED_DOCS_DIR = "stored_docs"
os.makedirs(STORED_DOCS_DIR, exist_ok=True)
app.mount("/documents", StaticFiles(directory=STORED_DOCS_DIR), name="documents")

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"status": "Precedent System Online"}

@app.get("/uploads/")
def list_uploads():
    """
    List all uploaded files with metadata.
    """
    files = []
    if os.path.exists(STORED_DOCS_DIR):
        for filename in os.listdir(STORED_DOCS_DIR):
            if filename.startswith("."): continue # Skip hidden files
            
            filepath = os.path.join(STORED_DOCS_DIR, filename)
            stats = os.stat(filepath)
            
            files.append({
                "filename": filename,
                "upload_time": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "uploaded_by": "Admin" # Placeholder for now
            })
            
    # Sort by newest first
    files.sort(key=lambda x: x['upload_time'], reverse=True)
    return files

@app.post("/ingest/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF or Text file to extract decisions from.
    """
    try:
        # Save to stored_docs for persistent access
        file_location = f"{STORED_DOCS_DIR}/{file.filename}"
        with open(file_location, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Trigger ingestion
        ingest_file(file_location)
        
        # Do NOT delete the file
        
        return {"message": f"Successfully processed {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/", response_model=list[SearchResult])
def search_memory(query: SearchQuery):
    """
    Search for past decisions.
    """
    try:
        return search_decisions(query)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
