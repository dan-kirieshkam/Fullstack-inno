from streamlit import session_state
import streamlit as st
# Функция которая сохраняет в памяти приложение информацию о пользователе: access_token
def login_with_session_state_saving(data: dict):
    session_state["access_token"] = data["access_token"]
    return session_state