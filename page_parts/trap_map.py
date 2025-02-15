import streamlit as st
import pydeck as pdk
from azure_.cosmosdb import search_container_by_query
import pandas as pd


def sample_trap_data():
    trap_data = [
        {
            "latitude": 34.600521,
            "longitude": 137.121363,
            "trap_name": "花の村ソーラーの道",
            "status": "稼働中",
            "id": "Trap-001",
        },
        {
            "latitude": 34.606175,
            "longitude": 137.109573,
            "trap_name": "ハラサワ",
            "status": "稼働中",
            "id": "Trap-002",
        },
        {
            "latitude": 34.610929,
            "longitude": 137.113483,
            "trap_name": "アキモトさんの檻",
            "status": "停止中",
            "id": "Trap-003",
        },
        {
            "latitude": 34.596175,
            "longitude": 137.123857,
            "trap_name": "花の村駐車場横",
            "status": "稼働中",
            "id": "Trap-004",
        },
        {
            "latitude": 34.597054,
            "longitude": 137.126528,
            "trap_name": "花の村の奥",
            "status": "撤去済み",
            "id": "Trap-005",
        },
    ]
    return trap_data


database_name = "sat-db"
container_name = "traps"


def call_trap_date():
    query = "SELECT c.id, c.users, c.task_date, c.trap_type, c.trap_name, c.latitude, c.longitude, c.number, c.status FROM c"
    parameters = []
    res = search_container_by_query(
        database_name,
        container_name,
        query,
        parameters,
    )
    return res


def trap_map(width=400, height=300, mode="稼働中", multi_select="multi-object"):
    trap_data = st.session_state.trap_data
    # trap_data = sample_trap_data()

    if not trap_data:
        st.warning("トラップデータがありません。")
        return

    # データをデータフレームに変換
    trap_data = pd.DataFrame(trap_data)

    # モードに基づいてデータをフィルタリング
    if mode != "すべて":
        trap_data = trap_data[trap_data["status"] == mode]

    # カラーの設定（事前にデータフレームへカラム追加）
    trap_data["color"] = [[0, 255, 0]] * len(trap_data)  # デフォルトカラー（緑色）
    for idx, row in trap_data.iterrows():
        if row["status"] == "稼働中":
            trap_data.at[idx, "color"] = [0, 0, 255, 160]  # 青色
        elif row["status"] == "停止中":
            trap_data.at[idx, "color"] = [255, 255, 0, 160]  # 黄色
        elif row["status"] == "撤去済み":
            trap_data.at[idx, "color"] = [225, 0, 0, 160]  # 赤色

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=trap_data,
        get_position="[longitude, latitude]",
        get_radius=50,
        get_color="color",
        pickable=True,
        auto_highlight=True,
        id="map",
    )

    # 初期表示の設定
    view_state = pdk.ViewState(
        latitude=34.614375,
        longitude=137.144072,
        zoom=12,
    )

    # Pydeckチャートを表示
    chart = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/satellite-v9",
        tooltip={"text": "{trap_name}"},
    )

    st.caption("🔵稼働中  🟡停止中  🔴撤去済み")
    event = st.pydeck_chart(
        chart,
        selection_mode=multi_select,  # single-objectにするときは,
        on_select="rerun",
        width=width,
        height=height,
    )
    if event.selection["objects"] == {}:
        st.session_state.selected_objects = {"map": []}
    else:
        st.session_state.selected_objects = event.selection["objects"]
    # print("event.selection==>")
    # print(event.selection)
    # print("st.session_state.selected_objects==>")
    # print(st.session_state.selected_objects)
    if st.session_state.selected_objects:
        for p in st.session_state.selected_objects["map"]:
            st.write(p["trap_name"])
