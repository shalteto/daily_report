import streamlit as st
from page_parts.trap_set import trap_set

st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")


def main():
    trap_set()


if __name__ == "__main__":
    main()
