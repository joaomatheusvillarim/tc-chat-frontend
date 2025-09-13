"""
Módulo para login.

POST /login
retorna o objeto que será salvo em st.session_state.user
"""
import requests
import json


def post_login(email: str,
               password: str) -> dict:
    import os
    backend_url = os.getenv("BACKEND_URL") or "http://localhost:10000"
    url = f"{backend_url}/login"
    try:
        response = requests.request("POST",
                                    url,
                                    json={
                                        "email": email,
                                        "password": password,
                                    },
                                    headers={
                                        "Content-Type": "application/json"
                                    })
        response.raise_for_status()
        result = json.loads(response.content.decode("utf-8"))
        return {
            "success": True,
            "result": result
        }
    except requests.HTTPError:
        message = json.loads(response.content.decode("utf-8"))["error"]
        return {
            "success": False,
            "message": message
        }
