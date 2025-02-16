import streamlit as st
from azure_.cosmosdb import upsert_to_container
from azure_.cosmosdb import search_container_by_query
from page_parts.edit_report import edit_report

database_name = "sat-db"
container_name = "daily_report"


def get_daily_report(task_type):
    # 本年のオーダー数をカウントする
    query = "SELECT * FROM c WHERE c.task_type = @task_type"
    parameters = [{"name": "@task_type", "value": task_type}]
    res = search_container_by_query(
        database_name,
        container_name,
        query,
        parameters,
    )
    return res


def main():
    edit_report()


if __name__ == "__main__":
    main()
