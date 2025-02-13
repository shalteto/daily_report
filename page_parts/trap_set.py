import streamlit as st
from azure_.cosmosdb import upsert_to_container
from tools.file_upload import file_upload
from tools.trap_id import count_trap

st.set_page_config(page_title="作業報告", layout="wide", page_icon="🐗")

def trap_set():
    st.title("罠設置🦌")
    with st.form(key="trap_set_form"):
        users = st.multiselect("従事者", st.session_state.users)
        st.write(
            "**１枚目の写真データ**から設置場所を取得します。必ず位置情報付きの設定で撮影してください"
        )
        uploaded_files = st.file_uploader(
            "写真をアップロード", accept_multiple_files=True, type=["jpg", "png"]
        )
        task_type = "罠設置"
        trap_name = st.text_input("罠の通称（地図に表示する名称）")
        trap_type = st.selectbox("罠種類", ["くくり", "箱", "ネット式囲い"])
        number = st.number_input(
            "設置数(同じスポット中の個数)", min_value=1, max_value=10, value=1
        )
        task_date = st.date_input("日付")
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        # uploaded_files が1つ以上で、users が1つ以上選択されている場合のみ処理を実行
        if uploaded_files and users and trap_name:
            file_names = file_upload(uploaded_files, task_type)
            # file_names の1つ目から位置情報を取得
            # サンプル：file_names={"file_name": uploaded_file.name, "latitude": lat, "longitude": lon}
            first_file = file_names[0]
            lat, lon = first_file["latitude"], first_file["longitude"]
            trap_count = count_trap()
            trap_count_str = str(trap_count + 1).zfill(3)  # 3桁の数値に変換
            trap_id = f"Trap-{trap_count_str}"
            data = {
                "id": trap_id,
                "users": users,
                "task_type": task_type,
                "task_date": task_date.strftime("%Y-%m-%d"),
                "trap_type": trap_type,
                "trap_name": trap_name,
                "latitude": lat,
                "longitude": lon,
                "number": number,
                "status": "稼働中",
            }
            try:
                database_name = "sat-db"
                container_name = "traps"
                upsert_to_container(database_name, container_name, data=data)
            except Exception as e:
                st.error(f"CosmosDB登録エラー: {e}")
                return
            st.success("送信完了")
        else:
            if not users:
                st.error("従事者を選択してください。")
            if not uploaded_files:
                st.error("写真をアップロードしてください。")
            if not trap_name:
                st.error("罠の通称を入力してください。")