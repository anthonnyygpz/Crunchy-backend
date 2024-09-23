from pydantic import BaseModel
from typing import Optional


class FileInfo(BaseModel):
    file_name: str
    content: str
    id_folder: str


class UploadInfo(BaseModel):
    file_path: str
    id_folder: str


class DownloadInfo(BaseModel):
    id_drive: str
    download_path: str


class SearchQuery(BaseModel):
    query: str


class MoveInfo(BaseModel):
    id_file: str
    id_folder: str


class FolderInfo(BaseModel):
    folder_name: str
    id_folder: Optional[str] = None


class PermissionInfo(BaseModel):
    id_drive: str
    type: str
    value: str
    role: str


class FolderContent(BaseModel):
    id: str
    title: str
    mimeType: str
    modifiedDate: str
