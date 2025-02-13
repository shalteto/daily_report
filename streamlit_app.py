# pip install streamlit
import streamlit as st
from st_init import init
from page_parts.upload_report import upload_report
from page_parts.trap_set import trap_set
from page_parts.input_order import input_order


st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")

def main():
    st.write("### 作業報告🐗")
    if st.sidebar.button("作業報告"):
        upload_report()
    if st.sidebar.button("罠設置"):
        trap_set()
    if st.sidebar.button("受注情報入力"):
        input_order()


if __name__ == "__main__":
    init()
    main()
