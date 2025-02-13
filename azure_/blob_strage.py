# pip install azure-storage-blob
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
import requests

# ストレージアカウント接続文字列
load_dotenv()
connection_string = os.getenv("BLOB_STORAGE_CONNECTION_STRING")


# def upload_blob(container_name, blob_name, data):
#     # BlobServiceClient のインスタンスを作成
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)

#     # コンテナクライアントを取得
#     container_client = blob_service_client.get_container_client(container_name)

#     # Blobをアップロード
#     try:
#         container_client.upload_blob(name=blob_name, data=data)
#         message = f"{blob_name} has been uploaded to {container_name} container."
#         print(message)
#     except Exception as e:
#         message = f"Failed to upload {blob_name} to {container_name} container."
#         print(message)
#         print(e)

#     return message


# Microsoft Entra ID の情報
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TARGET_USER = os.getenv("TARGET_USER")  # suzuki_shoichiro@atsumi-sat.com

def get_access_token():
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
    }
    response = requests.post(token_url, data=data)
    return response.json().get("access_token")

# def upload_to_onedrive(file_path, filename):
#     access_token = get_access_token()
#     if not access_token:
#         return "アクセストークン取得失敗"

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/octet-stream",
#     }
#     upload_url = f"https://graph.microsoft.com/v1.0/users/{TARGET_USER}/drive/root:/{filename}:/content"

#     with open(file_path, "rb") as file:
#         response = requests.put(upload_url, headers=headers, data=file)

#     return "✅ アップロード成功" if response.status_code in [200, 201] else f"❌ アップロード失敗: {response.text}"

def upload_blob(_, filename, uploaded_file):
    access_token = get_access_token()
    if not access_token:
        return "アクセストークン取得失敗"
    filename = "daily_report/" + filename
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
    }
    upload_url = f"https://graph.microsoft.com/v1.0/users/{TARGET_USER}/drive/root:/{filename}:/content"
    print(uploaded_file.name)
    response = requests.put(upload_url, headers=headers, data=uploaded_file)

    return "✅ アップロード成功" if response.status_code in [200, 201] else f"❌ アップロード失敗: {response.text}"
