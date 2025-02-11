import os
import requests
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

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

def upload_to_onedrive(file_path, filename):
    access_token = get_access_token()
    if not access_token:
        return "アクセストークン取得失敗"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
    }
    upload_url = f"https://graph.microsoft.com/v1.0/users/{TARGET_USER}/drive/root:/{filename}:/content"

    with open(file_path, "rb") as file:
        response = requests.put(upload_url, headers=headers, data=file)

    return "✅ アップロード成功" if response.status_code in [200, 201] else f"❌ アップロード失敗: {response.text}"

def upload_blob_to_onedrive(uploaded_file, filename):
    access_token = get_access_token()
    if not access_token:
        return "アクセストークン取得失敗"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
    }
    upload_url = f"https://graph.microsoft.com/v1.0/users/{TARGET_USER}/drive/root:/{filename}:/content"

    response = requests.put(upload_url, headers=headers, data=uploaded_file)

    return "✅ アップロード成功" if response.status_code in [200, 201] else f"❌ アップロード失敗: {response.text}"
