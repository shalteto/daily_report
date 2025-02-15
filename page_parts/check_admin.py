import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
admin_password = os.getenv("ADMIN_PASSWORD")


def check_admin():
    st.write("### 管理者ログイン")
    with st.form(key="admin_login_form"):
        is_admin_user = st.text_input(
            "管理者パスワードを入力してください", type="password"
        )
        submit_button = st.form_submit_button(label="ログイン")
        if submit_button:
            if is_admin_user == admin_password:
                print("password is correct")
                st.session_state.is_admin_user = True
            else:
                print("password is incorrect")
                st.session_state.is_admin_user = False
