import streamlit as st
import pandas as pd
from azure_.cosmosdb import upsert_to_container
from tools.file_upload import file_upload
from tools.trap_id import count_trap
from page_parts.trap_map import trap_map, call_trap_date


database_name = "sat-db"
container_name = "traps"


def trap_set():
    st.title("罠設置🦌")
    st.session_state.users_filtered_by_type = st.session_state.users.query(
        "trap == True"
    )["user_name"].tolist()
    with st.form(key="trap_set_form"):
        users = st.multiselect("従事者", st.session_state.users_filtered_by_type)
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
            first_file = file_names[0]
            lat, lon = first_file["latitude"], first_file["longitude"]
            trap_count = count_trap()
            trap_count_str = str(trap_count + 1).zfill(3)
            trap_id = f"Trap-{trap_count_str}"
            data = {
                "id": trap_id,
                "users": users,
                "task_date": task_date.strftime("%Y-%m-%d"),
                "trap_type": trap_type,
                "trap_name": trap_name,
                "latitude": lat,
                "longitude": lon,
                "number": number,
                "status": "稼働中",
            }
            try:
                upsert_to_container(database_name, container_name, data=data)
            except Exception as e:
                st.error(f"CosmosDB登録エラー: {e}")
                return
            st.success("送信完了")
            st.session_state.trap_data.append(
                {
                    "id": trap_id,
                    "users": users,
                    "task_date": task_date.strftime("%Y-%m-%d"),
                    "trap_type": trap_type,
                    "trap_name": trap_name,
                    "latitude": lat,
                    "longitude": lon,
                    "number": number,
                    "status": "稼働中",
                }
            )
        else:
            if not users:
                st.error("従事者を選択してください。")
            if not uploaded_files:
                st.error("写真をアップロードしてください。")
            if not trap_name:
                st.error("罠の通称を入力してください。")


def change_trap_status(map_data, status):
    # データからcolorカラムを除去し、statusを更新
    updated_data = []
    for data in map_data:
        data.pop("color")
        data["status"] = status
        updated_data.append(data)

    try:
        upsert_to_container(database_name, container_name, data=updated_data)
    except Exception as e:
        st.error(f"CosmosDB登録エラー: {e}")
        return
    st.session_state.trap_data = updated_data
    return True


def trap_stasus_change():
    st.title("罠状況変更🦌")

    trap_map_mode = st.selectbox(
        "表示する罠", ["すべて", "稼働中", "停止中", "撤去済み"], index=1
    )
    trap_map(mode=trap_map_mode)

    # オブジェクト部分を取得
    print("st.session_state.selected_objects==>")
    print(st.session_state.selected_objects)

    # 選択中の罠をデータフレームで表示するとき
    # if "map" in st.session_state.selected_objects:
    #     objects = st.session_state.selected_objects["map"]
    #     df = pd.DataFrame(objects)
    #     st.dataframe(df)

    col1, col2, col3 = st.columns(3)
    success = False
    st.text("選択中の罠を押したボタンの状況に切り替える")
    with col1:
        if st.button("稼働中"):
            success = change_trap_status(
                st.session_state.selected_objects["map"], "稼働中"
            )
    with col2:
        if st.button("停止中"):
            success = change_trap_status(
                st.session_state.selected_objects["map"], "停止中"
            )
    with col3:
        if st.button("撤去済み"):
            success = change_trap_status(
                st.session_state.selected_objects["map"], "撤去済み"
            )
    if success == True:
        st.success("罠の状況を変更しました")
        if st.button("罠マップの再読み込み"):
            st.rerun()
