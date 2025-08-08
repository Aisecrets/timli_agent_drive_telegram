"""Google Drive API tools for Timli.

Auth:
  - Use a *Service Account* JSON file (best for server-to-server).
  - Set env var GOOGLE_SERVICE_ACCOUNT_JSON to the absolute path of that JSON.
Structure:
  - Optionally set TIMLI_DRIVE_ROOT_FOLDER_ID to the Drive folder where all client folders live.
Notes:
  - Share the root folder with the service account email (from the JSON) as Editor.
"""
import io
import os
import json
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

def _service():
    sa_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_path or not os.path.exists(sa_path):
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON not set or file not found")
    creds = service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)

def _ensure_folder(name: str, parent: Optional[str]) -> str:
    """Find or create a folder by name under optional parent. Returns folder_id."""
    svc = _service()
    safe_name = name.replace("'", "\'")
    q = f"name = '{safe_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if parent:
        q += f" and '{parent}' in parents"
    res = svc.files().list(q=q, fields="files(id,name)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent:
        meta["parents"] = [parent]
    folder = svc.files().create(body=meta, fields="id").execute()
    return folder["id"]

def ensure_client_folder(client_name: str) -> str:
    """Ensure the client folder exists under TIMLI_DRIVE_ROOT_FOLDER_ID; return folder_id."""
    root = os.environ.get("TIMLI_DRIVE_ROOT_FOLDER_ID")
    safe = client_name.strip().replace("/", "_")
    return _ensure_folder(safe, root)

def upload_pdf_bytes(pdf_bytes: bytes, client_name: str, filename: str) -> str:
    """Upload raw PDF bytes into the client's folder. Returns webViewLink."""
    folder_id = ensure_client_folder(client_name)
    svc = _service()
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    media = MediaIoBaseUpload(io.BytesIO(pdf_bytes), mimetype="application/pdf", resumable=False)
    file_meta = {"name": filename, "parents": [folder_id]}
    file = svc.files().create(body=file_meta, media_body=media, fields="id,webViewLink").execute()
    return file["webViewLink"]

def write_json(client_name: str, data: dict, filename: str = "info.json") -> str:
    """Write a JSON file into the client's folder (create or overwrite). Returns webViewLink."""
    folder_id = ensure_client_folder(client_name)
    svc = _service()
    q = f"name = '{filename}' and '{folder_id}' in parents and trashed = false"
    found = svc.files().list(q=q, fields="files(id)").execute().get("files", [])
    content = io.BytesIO(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
    media = MediaIoBaseUpload(content, mimetype="application/json", resumable=False)
    if found:
        file_id = found[0]["id"]
        file = svc.files().update(fileId=file_id, media_body=media, fields="id,webViewLink").execute()
    else:
        meta = {"name": filename, "parents": [folder_id]}
        file = svc.files().create(body=meta, media_body=media, fields="id,webViewLink").execute()
    return file["webViewLink"]

def find_document_link(client_name: str, name_contains: str) -> str:
    """Return the first matching file's webViewLink within the client's folder."""
    folder_id = ensure_client_folder(client_name)
    svc = _service()
    safe = name_contains.replace("'", "\'")
    q = f"'{folder_id}' in parents and trashed = false and name contains '{safe}'"
    res = svc.files().list(q=q, fields="files(id,name,webViewLink)").execute()
    files = res.get("files", [])
    if not files:
        return ""
    return files[0]["webViewLink"]
