import requests
import streamlit as st

from api.client import (
    add_favorite,
    delete_item,
    get_error_message,
    remove_favorite,
)
from auth.state import is_admin, is_authenticated

# st.html("""
# <style>
#     /* Внешний контейнер */
#     .outer-container {
#         background-color: rgba(50, 50, 100, 0.2);
#         border-radius: 16px;
#         padding: 1.5rem;
#         border: 1px solid rgba(100, 100, 200, 0.2);
#         margin-bottom: 1rem;
#         transition: all 0.3s;
#     }
#     .outer-container:hover {
#         background-color: rgba(50, 50, 100, 0.3);
#         border-color: rgba(100, 100, 200, 0.4);
#     }
    
#     /* Внутренний контейнер */
#     .inner-container {
#         background-color: rgba(100, 100, 200, 0.25);
#         border-radius: 12px;
#         padding: 1rem;
#         border-left: 4px solid #2563EB;
#     }
    
#     /* Стили для изображений внутри внутреннего контейнера */
#     .inner-container img {
#         border-radius: 8px;
#         margin-top: 0.5rem;
#     }
# </style>
# """)

def render_favorite_button(item: dict, key_prefix: str) -> None:
    if not is_authenticated():
        st.caption("Войдите, чтобы добавить запись в избранное.")
        return

    item_id = item["id"]
    is_favorite = item.get("favorites", False)
    # st.write(is_favorite)
    button_text = "Убрать из избранного" if is_favorite else "В избранное"

    if st.button(button_text, key=f"{key_prefix}_favorite_{item_id}"):
        try:
            if is_favorite:
                response = remove_favorite(item_id)
            else:
                response = add_favorite(item_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.rerun()
        else:
            st.error(get_error_message(response))


def render_admin_actions(item_id: int, key_prefix: str) -> None:
    if not is_admin():
        return

    edit_column, delete_column = st.columns(2)

    if edit_column.button(
        "Редактировать",
        key=f"{key_prefix}_edit_{item_id}",
    ):
        st.session_state["edit_item_id"] = item_id
        st.switch_page("pages/edit_item.py")

    if delete_column.button(
        "Удалить",
        key=f"{key_prefix}_delete_{item_id}",
        type="primary",
    ):
        try:
            response = delete_item(item_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.success("Запись удалена.")
            st.switch_page("pages/catalog.py")
        else:
            st.error(get_error_message(response))


def render_item_card(item: dict) -> None:
    item_id = item["id"]

    with st.container(border=True):

        # st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQJXWxNKAzrp2QF3FeuIJfRVchRzRJ4oF74YwEgMGnCA&s=10", use_container_width=True)
        with st.container(border=True):
            if item.get("thumbnail"):
                st.image(item["thumbnail"])
            else:
                st.info("Изображение не добавлено")
            st.subheader(item["title"])
        st.write(item["short_description"])

        render_favorite_button(item, key_prefix="card")

        if st.button("Подробнее", key=f"card_details_{item_id}"):
            st.session_state["selected_item_id"] = item_id
            st.switch_page("pages/details.py")

        render_admin_actions(item_id, key_prefix="card")



def render_item_card_for_fav(item: dict) -> None:
    item_id = item["id"]

    with st.container(border=True):
        st.subheader(item["title"])
        st.write(item["short_description"])

        render_favorite_button(item, key_prefix="card")
        if st.button("Подробнее", key=f"card_details_{item_id}"):
            st.session_state["selected_item_id"] = item_id
            st.switch_page("pages/details.py")

        render_admin_actions(item_id, key_prefix="card")