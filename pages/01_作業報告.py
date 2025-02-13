import streamlit as st
from page_parts.upload_report import upload_report

st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")

def main():
    upload_report()

if __name__ == "__main__":
    main()