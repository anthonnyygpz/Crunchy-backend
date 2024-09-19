from pydantic import BaseModel
from typing import Optional


class FileInfo(BaseModel):
    nombre_archivo: str
    contenido: str
    id_folder: str


class UploadInfo(BaseModel):
    ruta_archivo: str
    id_folder: str


class DownloadInfo(BaseModel):
    id_drive: str
    ruta_descarga: str


class SearchQuery(BaseModel):
    query: str


class MoveInfo(BaseModel):
    id_archivo: str
    id_folder: str


class FolderInfo(BaseModel):
    nombre_carpeta: str
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
