import streamlit as st
from page_parts.trap_set import trap_set, trap_stasus_change
from page_parts.trap_map import call_trap_date

st.set_page_config(page_title="わな設置", layout="wide", page_icon="🐗")


def main():
    if st.session_state.trap_data == "":
        st.session_state.trap_data = call_trap_date()
    st.title("わな設置・状況変更")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("新規設置"):
            st.session_state.trap_page = "new_trap"
    with col2:
        if st.button("停止・撤去"):
            st.session_state.trap_page = "status_change"
    with col3:
        if st.button("名前・個数変更"):
            st.session_state.trap_page = "trap_edit"

    if st.session_state.trap_page == "None":
        st.text("上のボタンを教えてください")
    if st.session_state.trap_page == "new_trap":
        trap_set()
    if st.session_state.trap_page == "status_change":
        trap_stasus_change()


if __name__ == "__main__":
    main()
