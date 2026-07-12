import streamlit as st

row1 = st.columns(3)
row2 = st.columns(3)

for i, col in enumerate(row1 + row2):
    print(i, col)
    tile = col.container(key=f"container{i}", border=True, horizontal_alignment="center", vertical_alignment="center")
    tile.title("Книжка")
    tile.badge("❤️ Избранное", color="red")
    tile.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRggmpieE5NR7wYmvRst59UvRj3n-yE0ffdXpj7MArKHg&s")
    if tile.button("Подробнее", key=f"btn{i}"):
        tile.switch_page("pages/book1.py")
