
import requests

def get_backend():
    import os
    backend_url = os.getenv("BACKEND_URL") or "http://localhost:10000"
    try:
        response = requests.get(backend_url)
        return True
    except:
        return False