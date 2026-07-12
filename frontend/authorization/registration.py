import streamlit as st
from streamlit import session_state


st.set_page_config(page_title="Логин")


with st.form("registration_form", border=True):
    f"# Введите логин и пароль"
    st.subheader("Логин")
    login = st.text_input("Логин", value=session_state.get("login"), placeholder="Введите логин...")

    st.subheader("Пароль")
    psw = st.text_input("Пароль", key="psw", value=session_state.get("psw"), placeholder="Введите пароль...")

    st.subheader("Введите пароль ещё раз")
    psw = st.text_input("Пароль", key="repeat_psw", value=session_state.get("psw"), placeholder="Введите пароль...")

    submitted = st.form_submit_button("Регистрация")
    if submitted:
        st.switch_page("pages/app.py")
