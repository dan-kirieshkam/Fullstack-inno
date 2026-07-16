import streamlit as st
import random

with st.container(border=True):
    st.badge("избранное:", color="red")
    st.write("кошка:")
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQJXWxNKAzrp2QF3FeuIJfRVchRzRJ4oF74YwEgMGnCA&s=10")  
phrases = [
    "Спасибо! Кошка рада!",
    "Вау, кошка счастлива!",
    "Кошка благодарна вам!",
    "Кошка любит вас!",
    "Продолжай!",
    ":)",
    "Мурлычит... походу нравится",
    "Кошка обажает вас!"
]
if st.button("Погладить"):
    st.toast(random.choice(phrases))
    st.balloons()