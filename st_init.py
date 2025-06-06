import streamlit as st
import pandas as pd
from page_parts.input_users import load_users
from page_parts.trap_map import call_trap_date


def init():
    if "is_admin_user" not in st.session_state:
        st.session_state.is_admin_user = "None"
        print("INIT実行")
    if "selected_objects" not in st.session_state:
        st.session_state.selected_objects = ""
    if "users" not in st.session_state:
        st.session_state.users = load_users()
    if "users_filtered_by_type" not in st.session_state:
        st.session_state.users_filtered_by_type = ""
    if "user_input_type" not in st.session_state:
        st.session_state.user_input_type = "None"
    if "trap_page" not in st.session_state:
        st.session_state.trap_page = "None"
    if "trap_data" not in st.session_state:
        st.session_state.trap_data = ""
    if "daily_report_result_df" not in st.session_state:
        st.session_state.daily_report_result_df = pd.DataFrame()
    if "location" not in st.session_state:
        st.session_state.location = ""
