import streamlit as st
import pandas as pd
from azure_.cosmosdb import upsert_to_container
from azure_.cosmosdb import search_container_by_query

database_name = "sat-db"
container_name = "users"


def count_users():
    query = "SELECT VALUE COUNT(1) FROM c"
    parameters = []
    res = search_container_by_query(
        database_name,
        container_name,
        query,
        parameters,
    )
    count = res[0] if res else 0
    return count


def load_users():
    query = "SELECT c.user_name, c.gun, c.trap, c.net, c.other, c.id FROM c"
    parameters = []
    res = search_container_by_query(
        database_name,
        container_name,
        query,
        parameters,
    )
    if res:
        user_list = []
        user_list = pd.DataFrame(res, index=None)  # インデックスをなしに設定
        user_list = user_list.sort_values(by="id")
        return user_list


def rename_columns(df):
    df = df.rename(
        columns={
            "user_name": "従事者名",
            "gun": "銃猟",
            "trap": "罠猟",
            "net": "網猟",
            "other": "他",
            "id": "ID",
        }
    )
    return df


def re_rename_columns(df):
    df = df.rename(
        columns={
            "従事者名": "user_name",
            "銃猟": "gun",
            "罠猟": "trap",
            "網猟": "net",
            "他": "other",
            "ID": "id",
        }
    )
    return df


def list_users():
    st.write("### ユーザー一覧")
    with st.form(key="edit_form"):
        edit_rec = st.data_editor(
            rename_columns(st.session_state.users), hide_index=True
        )
        submit_button = st.form_submit_button(label="更新")
    if submit_button:
        edit_user(re_rename_columns(edit_rec), st.session_state.users)


def edit_user(edit_rec, original_list):
    data_list = []
    updated_users = []
    for _, row in edit_rec.iterrows():
        original_row = original_list[original_list["id"] == row["id"]]
        if not original_row.empty:
            original_row = original_row.iloc[0]
            if not row.equals(original_row):
                data = {
                    "id": row["id"],
                    "user_name": row["user_name"],
                    "gun": row["gun"],
                    "trap": row["trap"],
                    "net": row["net"],
                    "other": row["other"],
                }
                data_list.append(data)
                updated_users.append(row["user_name"])
                st.session_state.users.loc[
                    st.session_state.users["id"] == row["id"], :
                ] = pd.DataFrame([row])
                print(f"従事者: {row['user_name']} の更新完了")
            else:
                print(f"従事者: {row['user_name']} は変更されていません")
        else:
            st.error(f"ID: {row['id']} が見つかりません")

    if data_list:
        upsert_to_container(database_name, container_name, data_list)
        st.success(f"更新完了: {', '.join(updated_users)}")
        if st.button("名簿再読み込み"):
            st.rerun()


def input_user():
    st.write("### 新規入力")
    with st.form(key="users_form"):
        user_name = st.text_input("従事者名")
        st.text("従事者種別を選択")
        gun = st.checkbox("銃猟")
        trap = st.checkbox("罠猟")
        net = st.checkbox("網猟")
        other = st.checkbox("上記以外")
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        if user_name and (gun or trap or net or other):
            user_count = count_users()
            user_count_str = str(user_count + 1).zfill(3)
            data = {
                "id": f"USER-{user_count_str}",
                "user_name": user_name,
                "gun": gun,
                "trap": trap,
                "net": net,
                "other": other,
            }
            upsert_to_container(database_name, container_name, data)
            # メモリ上のデータを更新
            new_user = pd.DataFrame([data])
            st.session_state.users = pd.concat(
                [st.session_state.users, new_user], ignore_index=True
            )
            st.success("送信完了")
            st.text("追加入力：新規登録ボタンを押す")
        else:
            if not user_name:
                st.error("従事者名を選択してください。")
            if not (gun or trap or net or other):
                st.error("従事者種別を選択してください。")


def user_main():
    st.title("ユーザー情報入力🦋")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("新規登録"):
            st.session_state.user_input_type = "new"
            st.rerun()
    with col2:
        if st.button("一覧表示"):
            st.session_state.user_input_type = "list"
    if st.session_state.user_input_type == "new":
        input_user()
    elif st.session_state.user_input_type == "list":
        list_users()
    else:
        st.write("いずれかのボタンを押してください")
