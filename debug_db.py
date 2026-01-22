from backend.qdrant_client_wrapper import db_client
from backend.config import settings

print(f"Checking collection: {settings.COLLECTION_NAME}")
try:
    count = db_client.client.count(collection_name=settings.COLLECTION_NAME)
    print(f"Total points in DB: {count.count}")
    
    if count.count > 0:
        print(">> Database is populated.")
        # Perform a test search
        print("Attempting test search for 'AWS'...")
        results = db_client.query_points(
            collection_name=settings.COLLECTION_NAME,
            query=[0.1]*384, # Dummy vector
            limit=5
        ).points
        print(f"Found {len(results)} raw results.")
    else:
        print(">> Database is EMPTY. Please upload a file.")

except Exception as e:
    print(f"Error: {e}")
