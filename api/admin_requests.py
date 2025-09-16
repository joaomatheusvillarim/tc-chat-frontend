"""
Módulo para requisições de rotas de admin.
"""
import requests
import json


def base_admin_request(method: str,
                       token: str,
                       route: str,
                       data: dict = None):
    import os
    backend_url = os.getenv("BACKEND_URL") or "http://localhost:10000"
    url = f"{backend_url}/rest/admin/{route}"
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
        message = json.loads(response.content.decode("utf-8"))["message"]
        return {
            "success": True,
            "result": message
        }
    except requests.HTTPError:
        message = json.loads(response.content.decode("utf-8"))["error"]
        return {
            "success": False,
            "message": message
        }


def change_daily_quota_reset_value(reset_value: int,
                                   token: str):
    return base_admin_request(
        "PUT",
        token,
        "changeDailyQuotaResetValue",
        {
            "resetValue": reset_value
        }
    )


def run_daily_quota_reset(token: str):
    return base_admin_request(
        "POST",
        token,
        "runDailyQuotaReset",
    )


def change_all_users_authorization(is_authorized: bool,
                                   token: str):
    return base_admin_request(
        "PUT",
        token,
        "changeAllUsersAuthorization",
        {
            "isAuthorized": is_authorized
        }
    )
