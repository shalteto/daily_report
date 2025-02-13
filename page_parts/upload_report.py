import streamlit as st
from azure_.cosmosdb import upsert_to_container
from tools.file_upload import file_upload
from page_parts.trap_map import trap_map
from datetime import datetime, timedelta


def common_form_elements():
    users = st.multiselect("ユーザーを選択", st.session_state.users)
    task_date = st.date_input("作業日を選択")
    uploaded_files = st.file_uploader(
        "写真をアップロード", accept_multiple_files=True, type=["jpg", "png"]
    )
    now = datetime.now() + timedelta(hours=9)
    st.write(now)
    minuit = st.text_input("作業時間を分数で入力", 60)
    start_time = now - timedelta(minutes=int(minuit))
    end_time = now
    return users, task_date, uploaded_files, start_time, end_time


def common_animal_details():
    sex = st.selectbox("雌雄", ["オス", "メス"])
    size = st.slider("頭胴長サイズ（cm）", 0, 150, 50)
    weight = st.slider("推定体重（kg）", 0, 150, 50)
    disposal = st.selectbox("処分方法", ["焼却", "自家消費", "埋設", "食肉加工"])
    return sex, size, weight, disposal


def submit_data(data):
    try:
        database_name = "sat-db"
        container_name = "daily_report"
        upsert_to_container(database_name, container_name, data=data)
    except Exception as e:
        st.error(f"CosmosDB登録エラー: {e}")
        return
    st.success("送信完了")


def mimawari_form(task_type):
    trap_map()
    with st.form(key="mimawari_form"):
        users, task_date, uploaded_files, start_time, end_time = common_form_elements()
        if "map" not in st.session_state.selected_objects:
            trap = []
        else:
            trap = [obj["id"] for obj in st.session_state.selected_objects["map"]]
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        if uploaded_files and users:
            file_names = file_upload(uploaded_files, task_type)
            data = {
                "users": users,
                "task_type": task_type,
                "task_date": task_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "trap": trap,
                "file_names": file_names,
            }
            submit_data(data)
        else:
            if not users:
                st.error("従事者を選択してください。")
            if not uploaded_files:
                st.error("写真をアップロードしてください。")


def trap_hokaku_form(task_type):
    trap_map()
    with st.form(key="trap_hokaku_form"):
        st.write("入力は１頭ずつ行って下さい")
        users, task_date, uploaded_files, start_time, end_time = common_form_elements()
        sex, size, weight, disposal = common_animal_details()
        if "map" not in st.session_state.selected_objects:
            trap = []
        else:
            trap = [obj["id"] for obj in st.session_state.selected_objects["map"]]
        trap_type = st.selectbox("罠種類", ["くくり", "箱", "ネット式囲い"])
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        if uploaded_files and users:
            file_names = file_upload(uploaded_files, task_type)
            data = {
                "users": users,
                "task_type": task_type,
                "task_date": task_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "sex": sex,
                "size": size,
                "weight": weight,
                "disposal": disposal,
                "trap": trap,
                "trap_type": trap_type,
                "file_names": file_names,
            }
            submit_data(data)
        else:
            if not users:
                st.error("従事者を選択してください。")
            if not uploaded_files:
                st.error("写真をアップロードしてください。")


def gun_hokaku_form(task_type):
    with st.form(key="gun_hokaku_form"):
        users, task_date, uploaded_files, start_time, end_time = common_form_elements()
        sex, size, weight, disposal = common_animal_details()
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        if uploaded_files and users:
            file_names = file_upload(uploaded_files, task_type)
            data = {
                "users": users,
                "task_type": task_type,
                "task_date": task_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "sex": sex,
                "size": size,
                "weight": weight,
                "disposal": disposal,
                "file_names": file_names,
            }
            submit_data(data)
        else:
            if not users:
                st.error("従事者を選択してください。")
            if not uploaded_files:
                st.error("写真をアップロードしてください。")


def research_form(task_type):
    with st.form(key="research_hokaku_form"):
        users, task_date, uploaded_files, start_time, end_time = common_form_elements()
        comment = st.text_input("(任意) コメントを入力")
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        if uploaded_files and users:
            file_names = file_upload(uploaded_files, task_type)
            data = {
                "users": users,
                "task_type": task_type,
                "task_date": task_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "file_names": file_names,
                "comment": comment,
            }
            submit_data(data)
        else:
            if not users:
                st.error("従事者を選択してください。")
            if not uploaded_files:
                st.error("写真をアップロードしてください。")


def other_form(task_type):
    with st.form(key="other_hokaku_form"):
        users, task_date, uploaded_files, start_time, end_time = common_form_elements()
        comment = st.text_input("作業内容を入力")
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        if uploaded_files and users and comment:
            file_names = file_upload(uploaded_files, task_type)
            data = {
                "users": users,
                "task_type": task_type,
                "task_date": task_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "file_names": file_names,
                "comment": comment,
            }
            submit_data(data)
        else:
            if not users:
                st.error("従事者を選択してください。")
            if not uploaded_files:
                st.error("写真をアップロードしてください。")
            if not comment:
                st.error("作業内容を入力してください。")


def upload_report():
    st.title("作業報告🐗")
    task_type = st.selectbox(
        "作業種類を選択", ["見回り", "罠捕獲", "銃捕獲", "調査", "他"]
    )
    if task_type == "見回り":
        mimawari_form(task_type)
    elif task_type == "罠捕獲":
        trap_hokaku_form(task_type)
    elif task_type == "銃捕獲":
        gun_hokaku_form(task_type)
    elif task_type == "調査":
        research_form(task_type)
    elif task_type == "他":
        other_form(task_type)
    else:
        st.write("作業を選択してください")
