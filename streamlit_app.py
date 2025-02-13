# pip install streamlit
import streamlit as st
from st_init import init

st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")

def main():
    st.write("### 作業報告🐗")


if __name__ == "__main__":
    init()
    main()
