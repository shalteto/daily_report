import streamlit as st
from page_parts.input_order import input_order

st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")

def main():
    input_order()


if __name__ == "__main__":
    main()
