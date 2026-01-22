import sys
import os
import shutil
from backend.ingestion import ingest_file
from backend.qdrant_client_wrapper import db_client

# List of files to ingest
FILES = [
    "data/mock_data/2023_Cloud_Migration_Meeting.txt",
    "data/mock_data/2024_Database_Choice_Postgres_vs_Mongo.txt",
    "data/mock_data/2024_Remote_Work_Policy_Update.txt"
]

def main():
    print("Starting Manual Data Injection...")
    
    # Ensure DB is ready
    db_client.ensure_collection_exists()
    
    # 1. Ingest
    for file_path in FILES:
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            print(f"File not found: {abs_path}")
            continue
            
        print(f"Ingesting {file_path}...")
        try:
            ingest_file(abs_path)
        except Exception as e:
            print(f"Failed to ingest {file_path}: {e}")

    # 2. Verify Content (Peeking into Qdrant)
    print("\nVerifying Data Quality (Checking for Verbosity)...")
    try:
        results = db_client.search("AWS")
        if not results:
            print("No results found for 'AWS'")
        else:
            top_result = results[0]
            rationale = top_result.payload.get('rationale', [])
            print(f"\nResult Found: {top_result.payload.get('decision_title')}")
            print("\nRationale Sample (Check Length):")
            for point in rationale:
                word_count = len(point.split())
                status = "PASS" if word_count > 20 else "FAIL (Too Short)"
                print(f" - [{word_count} words] {status} : {point[:100]}...")
                
            if any(len(p.split()) > 20 for p in rationale):
                print("\nSUCCESS: Data is verbose!")
            else:
                print("\nWARNING: Data is still too short.")

    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    main()
