import streamlit as st
import main  # 사용자의 기존 로직 파일

st.title("나의 파이썬 앱")
st.write("코드는 숨겨져 있으며, 버튼을 누르면 실행됩니다.")

if st.button("실행하기"):
    result = main.start_logic() # main.py의 함수 호출
    st.success(f"결과: {result}")
