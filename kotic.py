import streamlit as st
import random
import numpy as np

with st.container(border=True):
    st.badge("избранное:", color="red")
    st.write("кошка:")
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQJXWxNKAzrp2QF3FeuIJfRVchRzRJ4oF74YwEgMGnCA&s=10")  
phrases = [
    "Спасибо! Кошка рада!",
    "Вау, кошка счастлива!",
    "Кошка благодарна вам!",
    "Кошка любит вас!",
    ":)",
    "Она обажает вас!"
]
st.button("Reset", type="primary")
if st.button("Погладить"):
    st.toast(random.choice(phrases))
    st.balloons()
    # st.feedback()

