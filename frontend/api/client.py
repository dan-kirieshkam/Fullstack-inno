from streamlit import session_state
import json

import requests

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"


def register(email, password):
    data = {"email": email, "password": password}
    with requests.Session() as s:
        response = s.post(REGISTER_ENDPOINT, json=data) # , headers={"Authorization": f"Bearer {token}"}

    return response.json()


def login(email, password):
    data = {"email": email, "password": password}

    with requests.Session() as s:
        response = s.post(LOGIN_ENDPOINT, json=data) # , headers={"Authorization": f"Bearer {token}"}

    return response.json()


def request_with_authorization_header(request_type: str, endpoint: str, params: dict = None, payload: dict = None) -> requests.Response:
    with requests.Session() as s:
        s.headers.update({"Authorization": f"Bearer {session_state['access_token']}"})
        if request_type == "POST":
            response = s.post(endpoint, json=payload)
        elif request_type == "GET":
            response = s.get(endpoint, params=params)
        elif request_type == "PUT":
            response = s.put(endpoint, json=payload)
        elif request_type == "DELETE":
            response = s.delete(endpoint, params=params)
    return response





if __name__ == '__main__':
    register_response = register()

    print(register_response)
    print(json.dumps(register_response, indent=4))

    login_response = login()
    print(login_response)
    print(json.dumps(login_response, indent=4))
