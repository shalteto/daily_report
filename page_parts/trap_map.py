import streamlit as st
import pydeck as pdk
from azure_.cosmosdb import search_container_by_query

date = {
    "id": "Trap-015",
    "users": ["宮田"],
    "task_type": "罠設置",
    "task_date": "2025-02-13",
    "trap_type": "くくり",
    "trap_name": "てすと",
    "latitude": 34.706623,
    "longitude": 137.355536,
    "number": 2,
    "status": "稼働中",
    "_rid": "mksDALkCVTwvAAAAAAAAAA==",
    "_self": "dbs/mksDAA==/colls/mksDALkCVTw=/docs/mksDALkCVTwvAAAAAAAAAA==/",
    "_etag": '"660041cc-0000-0800-0000-67adaff40000"',
    "_attachments": "attachments/",
    "_ts": 1739436020,
}


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
            "status": "稼働中",
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
            "status": "稼働中",
            "id": "Trap-005",
        },
    ]
    return trap_data


def call_trap_date():
    # 罠データを取得
    database_name = "sat-db"
    container_name = "traps"
    query = "SELECT c.latitude, c.longitude, c.trap_name, c.id  FROM c WHERE STARTSWITH(c.id, 'Trap-')"
    parameters = []
    res = search_container_by_query(
        database_name,
        container_name,
        query,
        parameters,
    )
    return res


def trap_map():
    trap_data = call_trap_date()
    # trap_data = sample_trap_data()
    print("trap_data==>")
    print(trap_data)
    # レイヤーを設定
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=trap_data,
        get_position="[longitude, latitude]",
        get_radius=50,
        get_color="[200, 30, 0, 160]",
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

    event = st.pydeck_chart(
        chart,
        selection_mode="multi-object",
        on_select="rerun",
    )

    # event.selection["objects"]
    st.session_state.selected_objects = event.selection["objects"]
    print("st.session_state.selected_objects==>")
    print(st.session_state.selected_objects)
    if st.session_state.selected_objects:
        for p in st.session_state.selected_objects["map"]:
            st.write(p["trap_name"])

    # 地図の表示
    # st.write("地図をクリックして座標を取得:")
