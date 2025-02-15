import streamlit as st
from datetime import datetime
from azure_.cosmosdb import upsert_to_container
from azure_.cosmosdb import search_container_by_query

database_name = "sat-db"
container_name = "orders"


def count_order(year):
    # 本年のオーダー数をカウントする
    query = "SELECT VALUE COUNT(1) FROM c WHERE c.year = @year"
    parameters = [{"name": "@year", "value": str(year)}]
    res = search_container_by_query(
        database_name,
        container_name,
        query,
        parameters,
    )
    count = res[0] if res else 0
    return count


def input_order():
    st.title("受注情報入力🦋")
    with st.form(key="order_form"):
        customer_name = st.text_input("発注元")
        order_name = st.text_input("事業名")
        area = st.text_input("実施地区")
        start_date = st.date_input("開始日")
        end_date = st.date_input("終了日")
        this_year = datetime.now().year
        order_year = st.number_input(
            "実施年度", min_value=1, max_value=this_year + 10, value=this_year
        )
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        if customer_name and order_name and area and start_date and end_date:
            order_count = count_order(order_year)
            order_count_str = str(order_count + 1).zfill(2)  # 2桁の数値に変換

            data = {
                "id": f"ORDER-{order_year}-{order_count_str}",
                "customer_name": customer_name,
                "order_name": order_name,
                "year": order_year,
                "area": area,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            }
            upsert_to_container(database_name, container_name, data)
            st.success("送信完了")
        else:
            if not customer_name:
                st.error("発注元を選択してください。")
            if not order_name:
                st.error("事業名を入力してください。")
            if not area:
                st.error("実施地区を入力してください。")
            if not start_date:
                st.error("開始日を入力してください。")
            if not end_date:
                st.error("終了日を入力してください。")
