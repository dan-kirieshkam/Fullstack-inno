import streamlit as st
from streamlit import session_state
from frontend.api import client


st.set_page_config(page_title="Логин")


with st.form("login_form", border=True):
    f"# Введите логин и пароль"
    st.subheader("Email")
    login = st.text_input("Email", value=session_state.get("login"), placeholder="Введите email...")

    st.subheader("Пароль")
    psw = st.text_input("Пароль", value=session_state.get("psw"), placeholder="Введите пароль...")

    submitted = st.form_submit_button("Войти", on_click=lambda email, psw: client.login(email, psw))
