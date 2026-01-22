import requests
import time

def check_api():
    base_url = "http://localhost:8000"
    print(f"Checking API at {base_url}...")
    
    # 1. Check Root
    try:
        r = requests.get(f"{base_url}/")
        if r.status_code == 200:
            print(">> Root Endpoint: OK")
        else:
            print(f">> Root Endpoint FAILED: {r.status_code}")
            return
    except Exception as e:
        print(f">> Could not connect to API: {e}")
        return

    # 1.5 Ingest a dummy file
    print("Checking Ingest Endpoint...")
    try:
        files = {'file': ('test_doc.txt', 'Decision: Use Groq. Rationale: It is fast and free.', 'text/plain')}
        r = requests.post(f"{base_url}/ingest/", files=files)
        if r.status_code == 200:
            print(">> Ingest Endpoint: OK")
        else:
            print(f">> Ingest Endpoint FAILED: {r.status_code} - {r.text}")
    except Exception as e:
        print(f">> Ingest Error: {e}")

    # 2. Check Search (with simple query)
    print("Checking Search Endpoint...")
    # time.sleep(2) # No wait needed if we assume DB is populated
    try:
        r = requests.post(f"{base_url}/search/", json={
            "query": "AWS",
            "limit": 5
        })
        if r.status_code == 200:
            data = r.json()
            print(f">> Search Endpoint: OK. Found {len(data)} results.")
            print(f"Response: {data}")
        else:
            print(f">> Search Endpoint FAILED: {r.status_code} - {r.text}")
    except Exception as e:
        print(f">> Search Error: {e}")

if __name__ == "__main__":
    check_api()
