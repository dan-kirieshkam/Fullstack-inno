import requests
import streamlit as st

from api.client import get_error_message, register


st.header("Регистрация")

with st.form("registration_form"):
    name1 = st.text_input("ФИО", key="registration_full_name")
    email1 = st.text_input("Почта", key="registration_email")
    password1 = st.text_input(
        "Пароль",
        type="password",
        key="registration_password",
    )
    submitted = st.form_submit_button("Зарегистрироваться")

if submitted:
    if not name1.strip() or not email1.strip() or not password1:
        st.error("Заполните все поля.")
        st.stop()

    try:
        response = register(
            email=email1.strip(),
            password=password1,
            name=name1.strip()
        )
    except requests.RequestException:
        st.error("Backend недоступен. Проверьте, запущен ли FastAPI.")
        st.stop()

    if response.status_code in (200, 201):
        st.success("Регистрация выполнена. Теперь войдите в аккаунт.")
        st.switch_page("pages/login.py")
    else:
        st.error(get_error_message(response))

st.page_link("pages/login.py", label="Уже есть аккаунт? Войти")