# pip install streamlit
import streamlit as st
from st_init import init
from page_parts.upload_report import upload_report
from page_parts.trap_set import trap_set
from page_parts.input_order import input_order


def main():
    st.text("合同会社ＳＡＴ")
    st.write("# 作業報告アプリ🐗🦌🦋")
    st.write('左上の"＞"でメニューを表示')


if __name__ == "__main__":
    init()
    main()
