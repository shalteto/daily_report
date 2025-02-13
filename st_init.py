import streamlit as st


def init():
    if "selected_objects" not in st.session_state:
        st.session_state.selected_objects = ""
    if "users" not in st.session_state:
        st.session_state.users = ["鈴木","宮田", "加藤", "伊藤"]
