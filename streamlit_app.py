# pip install streamlit
import streamlit as st
import time
from azure_.cosmosdb import upsert
from azure_.onedrive_file_upload import upload_blob_to_onedrive

st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")

def main():
    st.write("### 作業報告🐗")
    with st.form(key="task_form"):
        users = st.multiselect("ユーザーを選択", ["宮田", "加藤", "伊藤"])
        uploaded_files = st.file_uploader(
            "写真をアップロード", accept_multiple_files=True
        )
        task_type = st.selectbox("作業種類を選択", ["見回", "捕獲"])
        task_date = st.date_input("作業日を選択")
        task_description = st.text_area("作業内容を入力")
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        task_date = task_date.strftime("%Y-%m-%d")
        data = {
            "users": users,
            "task_type": task_type,
            "task_date": task_date,
            "task_description": task_description,
        }
        try:
            # アップロードされたファイルを OneDrive にアップロード
            index = 1
            # timestamp として20210901123456のような形式でデータ生成
            timestamp = time.strftime("%Y%m%d%H%M%S")

            for uploaded_file in uploaded_files:
                extension = "." + uploaded_file.name.split(".")[-1]
                filename = "daily_report/" +timestamp + "_" + task_type + str(index) + extension
                upload_blob_to_onedrive(uploaded_file, filename)
                index += 1
        except Exception as e:
            st.error(f"Blob登録エラー: {e}")
            return
        try:
            # Cosmos DB にデータを登録
            upsert(data)
        except Exception as e:
            st.error(f"CosmosDB登録エラー: {e}")
            return


if __name__ == "__main__":
    main()
