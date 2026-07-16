import streamlit as st
import cv2
import time

st.title("Счётчик FPS в реальном времени")
frame_placeholder = st.empty()
fps_text = st.empty()

cap = cv2.VideoCapture(0) # 0 для веб-камеры, либо путь к видеофайлу

prev_time = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        st.warning("Не удалось получить кадр.")
        break

    # --- Расчет FPS ---
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Конвертируем BGR (OpenCV) в RGB (Streamlit)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Отображаем кадр и FPS
    frame_placeholder.image(frame, channels="RGB", use_column_width=True)
    fps_text.write(f"**FPS:** {fps:.2f}")

cap.release()
