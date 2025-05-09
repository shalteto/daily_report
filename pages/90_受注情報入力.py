import streamlit as st
from page_parts.input_order import input_order
from page_parts.check_admin import check_admin

st.set_page_config(page_title="発注情報登録", layout="wide", page_icon="🐗")


def main():
    if st.session_state.is_admin_user == True:
        st.success("管理者ログイン中")
        input_order()
    else:
        st.warning("管理者ログインが必要です。")
        check_admin()

        if st.session_state.is_admin_user == True:
            print(st.session_state.is_admin_user)
            st.success("管理者ログイン成功")
            st.write("---")
            input_order()
        elif st.session_state.is_admin_user == False:
            st.error("パスワードがちがいます")
            st.session_state.is_admin_user = "None"
        elif st.session_state.is_admin_user == "None":
            st.write("")


if __name__ == "__main__":
    main()
