import requests
import streamlit as st

from api.client import get_error_message, get_item, update_item
from auth.state import require_admin


require_admin()
st.header("Редактирование записи")

item_id = st.session_state.get("edit_item_id")

if item_id is None:
    st.info("Сначала выберите запись для редактирования.")
    st.stop()

try:
    item_response = get_item(item_id)
except requests.RequestException:
    st.error("Не удалось получить запись с backend.")
    st.stop()

if not item_response.ok:
    st.error(get_error_message(item_response))
    st.stop()

item = item_response.json()

with st.form(f"edit_item_form_{item_id}"):
    title = st.text_input("Название", value=item["title"])
    # short_description = st.text_area(
    #     "Краткое описание",
    #     value=item.get("short_description", ""),
    # )
    # title = st.text_area(
    #     "Название",
    #     value=item.get("title", ""),
    # )
    publisher = st.text_area(
        "Автор",
        value=item.get("publisher", ""),
    )
    short_description = st.text_area(
        "Описание",
        value=item.get("short_description", ""),
    )
    image_url = st.text_input(
        "Ссылка на изображение",
        value=item.get("image_url") or "",
    )
    genre = st.text_area(
        "Жанр",
        value=item.get("genre", ""),
    )
    submitted = st.form_submit_button("Сохранить")

if submitted:
    if not title.strip():
        st.error("Укажите название.")
        st.stop()

    payload = {
        "title": title.strip(),
        "publisher": publisher.strip(),
        "short_description": short_description.strip(),
        "image_url": image_url.strip() or None,
        "genre": genre.strip(),
    }

    try:
        response = update_item(item_id, payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.ok:
        st.session_state["selected_item_id"] = item_id
        st.switch_page("pages/details.py")
    else:
        st.error(get_error_message(response))