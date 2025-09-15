"""
Módulo para perfil do usuário.

GET /users/:userId
PUT /users/:userId
retorna o objeto que será salvo em st.session_state.user
"""
import requests
import json


def base_user_request(method: str,
                      *,
                      token: str = "",
                      user_id: str = "",
                      data: dict = None):
    import os
    backend_url = os.getenv("BACKEND_URL") or "http://localhost:10000"
    url = f"{backend_url}/users/{user_id}"
    headers = None
    if token:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    try:
        response = requests.request(method,
                                    url,
                                    json=data,
                                    headers=headers)
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


def post_user(name: str,
              email: str,
              password: str) -> dict:
    return base_user_request(
        "POST",
        data={
            "name": name,
            "email": email,
            "password": password
        }
    )


def get_all_users(token: str):
    return base_user_request(
        "GET",
        token=token
    )


def get_user(user_id: int,
             token: str):
    return base_user_request(
        "GET",
        token=token,
        user_id=user_id
    )


def put_user(user_id: int,
             password: str,
             token: str):
    return base_user_request(
        "PUT",
        user_id=user_id,
        token=token,
        data={
            "password": password
        }
    )
