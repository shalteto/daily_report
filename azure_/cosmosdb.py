# pip install azure-cosmos
# pip install python-dotenv
from azure.cosmos import CosmosClient
from dotenv import load_dotenv
import os
import uuid

# .envファイルの読み込み
load_dotenv()

# Cosmos DB の接続情報
COSMOSDB_CORE_ENDPOINT = os.getenv("COSMOSDB_ENDPOINT")
COSMOSDB_CORE_API_KEY = os.getenv("COSMOSDB_KEY")


# cosmosclientの生成
def create_cosmos_client(
    endpoint: str, key: str, database_name: str, container_name: str
):
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return client, database, container


# データをCosmos DBに登録する
def upsert_to_container(database_name: str, container_name: str, data):
    _, _, container = create_cosmos_client(
        COSMOSDB_CORE_ENDPOINT, COSMOSDB_CORE_API_KEY, database_name, container_name
    )

    # データがリストの場合は複数レコードを登録
    if isinstance(data, list):
        for record in data:
            if "id" not in record:
                record["id"] = str(uuid.uuid4())
            container.upsert_item(body=record)
        return f"{len(data)} 件のデータを登録しました"

    # 単一レコードの場合
    if "id" not in data:
        data["id"] = str(uuid.uuid4())
    return container.upsert_item(body=data)


def search_container_by_query(
    database_name: str,
    container_name: str,
    query: str,
    parameters: list,
):
    _, _, container = create_cosmos_client(
        COSMOSDB_CORE_ENDPOINT, COSMOSDB_CORE_API_KEY, database_name, container_name
    )
    results = container.query_items(
        query=query, parameters=parameters, enable_cross_partition_query=True
    )
    return list(results)
