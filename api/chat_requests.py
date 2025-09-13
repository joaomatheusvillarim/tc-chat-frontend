"""
Módulo para requisições de chats do TC-chat.

GET /users/:user_id/chats
retorna o objeto que será salvo em st.session_state.userChats

POST /users/:user_id/chats
GET /users/:user_id/chats/:chat_id
PUT /users/:user_id/chats/:chat_id
retorna o objeto que será salvo em st.session_state.currentChat

DELETE /users/:user_id/chats/:chat_id
sem retorno
"""
import requests
import json


def format_messages(messages: list[dict]) -> list[dict]:
    """Recebe as mensagens no formato {prompt: string, response: string}[]
    do backend e tranforma em
    [
      {content: string, role: "user"},
      {content: string, role: "assistant"},
      ...
    ]
    """
    formattedMessages = []
    for message in messages:
        formattedMessages.append(
            {"role": "user", "content": message["prompt"]})
        formattedMessages.append(
            {"role": "assistant", "content": message["response"]})
    return formattedMessages


def base_chat_request(method: str,
                      token: str,
                      user_id: str,
                      *,
                      chat_id: str = "",
                      data: dict = None) -> requests.Response:
    import os
    backend_url = os.getenv("BACKEND_URL") or "http://localhost:10000"
    url = f"{backend_url}/users/{user_id}/chats/{chat_id}"
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


def post_chat(user_id: int,
              prompt: str,
              token: str) -> dict:
    return base_chat_request(
        "POST",
        token,
        str(user_id),
        data={
            "prompt": prompt
        }
    )


def put_chat(user_id: int,
             chat_id: int,
             prompt: str,
             token: str) -> dict:
    return base_chat_request(
        "PUT",
        token,
        str(user_id),
        chat_id=str(chat_id),
        data={
            "prompt": prompt
        }
    )


def get_chat(user_id: int,
             chat_id: int,
             token: str) -> dict:
    return base_chat_request(
        "GET",
        token,
        str(user_id),
        chat_id=str(chat_id)
    )


def get_all_chats(user_id: int,
                  token: str) -> dict:
    return base_chat_request(
        "GET",
        token,
        str(user_id)
    )
