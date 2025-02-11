# pip install azure-cosmos
# pip install python-dotenv
from azure.cosmos import CosmosClient
from dotenv import load_dotenv
import os
import uuid

# .envファイルの読み込み
load_dotenv()

# Cosmos DB の接続情報
ENDPOINT = os.getenv("COSMOSDB_ENDPOINT")
KEY = os.getenv("COSMOSDB_KEY")

# クライアントを作成
client = CosmosClient(ENDPOINT, KEY)


def upsert(data):
    # データベースとコンテナに接続
    database = client.get_database_client("sat-db")
    container = database.get_container_client("users")

    if "id" not in data:
        data["id"] = str(uuid.uuid4())

    container.create_item(body=data)
    print("データを挿入しました")
