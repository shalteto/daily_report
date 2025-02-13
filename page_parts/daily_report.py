import streamlit as st
import time
from azure_.cosmosdb import upsert_mimawari
from azure_.onedrive_file_upload import upload_blob_to_onedrive
from tools.gps import get_gps_coordinates, get_full_address

def daily_report():
    task_type = st.selectbox("作業種類を選択", ["見回", "捕獲"])
    if task_type == "見回":
        mimawari_report(task_type)
    elif task_type == "捕獲":
        st.write("捕獲")
        capture_report(task_type)  # コメントアウトを解除

def mimawari_report(task_type):
    with st.form(key="mimawari_task_form"):
        users = st.multiselect("作業者", st.session_state.users)
        uploaded_files = st.file_uploader(
            "写真をアップロード", accept_multiple_files=True
        )
        task_date = st.date_input("作業日を選択")

        # 画像がアップロードされている場合のみGPS情報を取得
        lat, lon, full_address, muniCd = None, None, None, None
        if uploaded_files:
            lat, lon = get_gps_coordinates(uploaded_files[0].read())
            full_address, muniCd = get_full_address(lat, lon)
            st.text(f"1枚目の写真で座標を取得: {full_address} / {lat}, {lon}")

        task_description = st.text_area("作業内容を入力")
        submit_button = st.form_submit_button(label="送信")

        if submit_button:
            # 写真の名称パスを作成してリストに格納
            photo_paths = []
            timestamp = time.strftime("%Y%m%d%H%M%S")
            for i, uploaded_file in enumerate(uploaded_files):
                extension = "." + uploaded_file.name.split(".")[-1]
                filename = "daily_report/" +timestamp + "_" + task_type + str(1+1) + extension
                photo_paths.append(filename)

            task_date = task_date.strftime("%Y-%m-%d")

            try:
                # アップロードされたファイルを OneDrive にアップロード
                i=0
                for i, uploaded_file in enumerate(uploaded_files):
                    upload_blob_to_onedrive(uploaded_file, photo_paths[i])
            except Exception as e:
                st.error(f"Blob登録エラー: {e}")
                return
            
            data = {
                "users": users,
                "task_type": task_type,
                "task_date": task_date,
                "trap_location": full_address,
                "task_description": task_description,
                "photo_path": photo_paths,
            }
            try:
                # Cosmos DB にデータを登録
                upsert_mimawari(data)
            except Exception as e:
                st.error(f"CosmosDB登録エラー: {e}")
                return
            st.success("送信完了")

def capture_report(task_type):
    with st.form(key="capture_task_form"):
        users = st.multiselect("作業者", st.session_state.users)
        uploaded_files = st.file_uploader(
            "写真をアップロード", accept_multiple_files=True
        )
        task_date = st.date_input("作業日を選択")

        # 画像がアップロードされている場合のみGPS情報を取得
        lat, lon, full_address, muniCd = None, None, None, None
        if uploaded_files:
            lat, lon = get_gps_coordinates(uploaded_files[0].read())
            full_address, muniCd = get_full_address(lat, lon)
            st.text(f"1枚目の写真で座標を取得: {full_address} / {lat}, {lon}")

        task_description = st.text_area("作業内容を入力")
        submit_button = st.form_submit_button(label="送信")

        if submit_button:
            # 写真の名称パスを作成してリストに格納
            photo_paths = []
            timestamp = time.strftime("%Y%m%d%H%M%S")
            for i, uploaded_file in enumerate(uploaded_files):
                extension = "." + uploaded_file.name.split(".")[-1]
                filename = "daily_report/" +timestamp + "_" + task_type + str(1+1) + extension
                photo_paths.append(filename)

            task_date = task_date.strftime("%Y-%m-%d")
            try:
                # アップロードされたファイルを OneDrive にアップロード
                i=0
                for i, uploaded_file in enumerate(uploaded_files):
                    upload_blob_to_onedrive(uploaded_file, photo_paths[i])

            except Exception as e:
                st.error(f"Blob登録エラー: {e}")
                return
            
            data = {
                "users": users,
                "task_type": task_type,
                "task_date": task_date,
                "trap_address": full_address,
                "muniCd": muniCd,
                "lat": lat,
                "lon": lon,
                "photo_path": photo_paths,
            }
            try:
                # Cosmos DB にデータを登録
                upsert_mimawari(data)
            except Exception as e:
                st.error(f"CosmosDB登録エラー: {e}")
                return
            st.success("送信完了")