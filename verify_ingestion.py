import sys
import os

# Ensure backend can be imported
sys.path.append(os.getcwd())

from backend.ingestion import ingest_file
from backend.qdrant_client_wrapper import db_client
from backend.models import SearchQuery
from backend.retrieval import search_decisions

def verify():
    print("--- Starting Verification ---")
    
    # 1. Ensure DB exists (Embeded)
    print("Step 1: Initializing Database...")
    db_client.ensure_collection_exists()
    
    # 2. Ingest Mock Data
    file_path = "data/mock_data/2023_Cloud_Migration_Meeting.txt"
    print(f"Step 2: Ingesting {file_path}...")
    try:
        ingest_file(file_path)
        print(">> Ingestion Successful!")
    except Exception as e:
        print(f">> Ingestion FAILED: {e}")
        return

    # 3. Search
    print("Step 3: Verifying Retrieval...")
    query = SearchQuery(query="Why AWS?", limit=1)
    results = search_decisions(query)
    
    if results:
        print(f">> Search Successful! Found {len(results)} result(s).")
        print(f"Top Result: {results[0].decision.decision_title}")
        print(f"Rationale: {results[0].decision.rationale}")
        print("--- Verification PASSED ---")
    else:
        print(">> Search FAILED: No results found.")

if __name__ == "__main__":
    verify()
