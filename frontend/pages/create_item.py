import requests
import streamlit as st

from api.client import create_item, get_error_message
from auth.state import require_admin


require_admin()
st.header("Новая запись")

with st.form("add_item_form"):
    title = st.text_input("Название")
    publisher = st.text_input("Автор")
    short_description = st.text_area("Полное описание")
    thumbnail = st.text_input("Ссылка на изображение")
    genre = st.text_input("Жанр")
    release_date = st.text_input("Дата релиза")
    submitted = st.form_submit_button("Создать")
    

if submitted:
    if not title.strip():
        st.error("Укажите название.")
        st.stop()

    payload = {
        "title": title.strip(),
        "publisher": publisher.strip(),
        "short_description": short_description.strip() or None,
        "thumbnail": thumbnail.strip() or None,
        "genre": genre.strip(),
        "release_date": release_date.strip(),
    }

    try:
        response = create_item(payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.status_code in (200, 201):
        created_item = response.json()
        st.session_state["selected_item_id"] = created_item["id"]
        st.switch_page("pages/details.py")
    else:
        st.error(get_error_message(response))

import streamlit as st
from api.client import create_item_with_image, get_error_message
from auth.state import is_admin

if not is_admin():
    st.error("Доступ запрещен")
    st.stop()

# st.header("Создать запись")

# with st.form("create_item_form"):
#     title = st.text_input("Название")
#     description = st.text_area("Описание")
#     prev = st.text_area("Краткое описание")
#     price = st.number_input("Цена", min_value=0.0, step=0.1)
    
#     # Загрузка картинки
#     uploaded_file = st.file_uploader(
#         "Загрузите изображение",
#         type=['png', 'jpg', 'jpeg', 'webp'],
#         help="Поддерживаются форматы: PNG, JPG, JPEG, WEBP"
#     )
    
#     # Превью загруженной картинки
#     if uploaded_file:
#         st.image(uploaded_file, use_container_width=True, caption="Превью")
    
#     submitted = st.form_submit_button("Создать")
    
#     if submitted:
#         if not title:
#             st.error("Название обязательно")
#             st.stop()
        
#         data = {
#             "title": title,
#             "description": description,
#             "prev": prev,
#             "price": price
#         }
        
#         try:
#             response = create_item_with_image(data, uploaded_file)
#             if response.ok:
#                 st.success("Запись создана!")
#                 st.switch_page("pages/catalog.py")
#             else:
#                 st.error(get_error_message(response))
#         except Exception as e:
#             st.error(f"Ошибка: {e}")