import requests
import streamlit as st

from api.client import get_error_message, get_favorites
from auth.state import require_login
from components.item_card import render_item_card, render_item_card_for_fav


require_login()
st.header("Избранное")

try:
    response = get_favorites()
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

data = response.json()

# Извлекаем список избранных игр из поля "favorites"
items = data.get("favorites", [])
total = data.get("total", 0)

if not items:
    st.info("В избранном пока ничего нет.")
    st.stop()

st.write(f"Всего в избранном: {total}")

for item in items:
    render_item_card_for_fav(item)