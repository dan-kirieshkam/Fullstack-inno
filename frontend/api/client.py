from streamlit import session_state
import requests

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"
PROFILE_ENDPOINT = f"{BACKEND_URL}/users/me/"
ITEMS_ENDPOINT = f"{BACKEND_URL}/games/"
FAVORITES_ENDPOINT = f"{BACKEND_URL}/favorites/"

API_URL = "http://localhost:8000"

def register(email: str, password: str, name: str) -> requests.Response:
    data = {
        "email": email,
        "password": password,
        "name": name,
        # "bursday": "2000-01-01",
        # "prev": "Нет данных",
    }
    return requests.post(REGISTER_ENDPOINT, json=data)


def login(email: str, password: str) -> requests.Response:
    data = {
        "email": email,
        "password": password,
    }
    return requests.post(LOGIN_ENDPOINT, json=data)


def request_with_authorization_header(
    request_type: str,
    endpoint: str,
    params: dict | None = None,
    payload: dict | None = None,
) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {session_state['access_token']}"
    }

    if request_type == "GET":
        response = requests.get(endpoint, headers=headers, params=params)
    elif request_type == "POST":
        response = requests.post(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "PATCH":
        response = requests.patch(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "DELETE":
        response = requests.delete(endpoint, headers=headers, params=params)
    else:
        raise ValueError("Неизвестный тип запроса")

    if response.status_code == 401:
        session_state.pop("access_token", None)
        session_state.pop("profile", None)
        session_state.pop("user_id", None)

    return response


def get_error_message(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка backend: HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка backend: HTTP {response.status_code}"


def get_profile() -> requests.Response:
    return request_with_authorization_header("GET", PROFILE_ENDPOINT)


def get_items() -> requests.Response:
    if session_state.get("access_token"):
        return request_with_authorization_header("GET", ITEMS_ENDPOINT)
    return requests.get(ITEMS_ENDPOINT)


def get_item(item_id: int) -> requests.Response:
    endpoint = f"{ITEMS_ENDPOINT}{item_id}/"
    if session_state.get("access_token"):
        return request_with_authorization_header("GET", endpoint)
    return requests.get(endpoint)


def get_favorites() -> requests.Response:
    """Получить избранные игры текущего пользователя"""
    endpoint = f"{FAVORITES_ENDPOINT}me/"
    return request_with_authorization_header("GET", endpoint)


def add_favorite(game_id: int) -> requests.Response:
    """Добавить игру в избранное"""
    user_id = session_state.get("user_id")
    if not user_id:
        profile = session_state.get("profile")
        if profile:
            user_id = profile.get("id")
    
    if not user_id:
        raise ValueError("User not logged in")
    
    payload = {
        "user_id": user_id,
        "game_id": game_id,
        "extra_data": None
    }
    return request_with_authorization_header("POST", FAVORITES_ENDPOINT, payload=payload)


def remove_favorite(game_id: int) -> requests.Response:
    """Удалить игру из избранного"""
    user_id = session_state.get("user_id")
    if not user_id:
        profile = session_state.get("profile")
        if profile:
            user_id = profile.get("id")
    
    if not user_id:
        raise ValueError("User not logged in")
    
    params = {
        "user_id": user_id,
        "game_id": game_id,
    }
    return request_with_authorization_header("DELETE", FAVORITES_ENDPOINT, params=params)


def create_item(payload: dict) -> requests.Response:
    return request_with_authorization_header(
        "POST",
        ITEMS_ENDPOINT,
        payload=payload,
    )


def update_item(item_id: int, payload: dict) -> requests.Response:
    endpoint = f"{ITEMS_ENDPOINT}{item_id}/"
    return request_with_authorization_header(
        "PATCH",
        endpoint,
        payload=payload,
    )


def delete_item(item_id: int) -> requests.Response:
    endpoint = f"{ITEMS_ENDPOINT}{item_id}/"
    return request_with_authorization_header("DELETE", endpoint)



def create_item_with_image(data, image_file=None):
    """Создание товара с картинкой"""
    if image_file:
        files = {"image": image_file}
        response = requests.post(f"{API_URL}/items/", data=data, files=files)
    else:
        response = requests.post(f"{API_URL}/items/", json=data)
    return response

def update_item_with_image(item_id, data, image_file=None):
    """Обновление товара с картинкой"""
    if image_file:
        files = {"image": image_file}
        response = requests.put(f"{API_URL}/items/{item_id}", data=data, files=files)
    else:
        response = requests.put(f"{API_URL}/items/{item_id}", json=data)
    return response