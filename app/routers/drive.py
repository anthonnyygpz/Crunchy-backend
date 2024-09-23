from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError

from app.schemas.drive import (
    FolderContent,
    FileInfo,
    UploadInfo,
    DownloadInfo,
    SearchQuery,
    MoveInfo,
    FolderInfo,
    PermissionInfo,
)


router = APIRouter()

credentials_directory = "credentials_module.json"


def login():
    GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = credentials_directory
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_directory)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(credentials_directory)
    credentials = GoogleDrive(gauth)
    return credentials


@router.get("/list_folder_contents/{folder_id}", response_model=List[FolderContent])
def list_folder_contents(folder_id: str):
    credentials = login()
    query = f"'{folder_id}' in parents and trashed=false"
    file_list = credentials.ListFile({"q": query}).GetList()

    content = []
    for file in file_list:
        content.append(
            FolderContent(
                id=file["id"],
                title=file["title"],
                mimeType=file["mimeType"],
                modifiedDate=file["modifiedDate"],
            )
        )

    return content


@router.post("/create_text_file/")
def create_text_file(file_info: FileInfo):
    credentials = login()
    file = credentials.CreateFile(
        {
            "title": file_info.file_name,
            "parents": [{"kind": "drive#fileLink", "id": file_info.id_folder}],
        }
    )
    file.SetContentString(file_info.content)
    file.Upload()
    return {"message": "Archivo creado exitosamente"}


@router.post("/file_upload/")
def subir_archivo(upload_info: UploadInfo):
    credentials = login()
    file = credentials.CreateFile(
        {"parents": [{"kind": "drive#fileLink", "id": upload_info.id_folder}]}
    )
    file["title"] = upload_info.file_path.split("/")[-1]
    file.SetContentFile(upload_info.file_path)
    file.Upload()
    return {"message": "Archivo subido exitosamente"}


@router.post("/download_file_by_id/")
def download_file_by_id(download_info: DownloadInfo):
    credentials = login()
    file = credentials.CreateFile({"id": download_info.id_drive})
    file_name = file["title"]
    file.GetContentFile(download_info.download_path + file_name)
    return {"message": f"Archivo {file_name} descargado exitosamente"}


@router.post("/search")
def search_files(search_query: SearchQuery):
    try:
        credentials = login()
        file_list = credentials.ListFile(
            {"q": f"title contains '{search_query.query}' and trashed=false"}
        ).GetList()
        results = [{"title": file["title"], "id": file["id"]} for file in file_list]
        return {"results": results}
    except ApiRequestError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al buscar en Google Drive: {str(e)}"
        )


@router.post("/delete_file/{id_file}")
def delete_file(id_file: str):
    credentials = login()
    file = credentials.CreateFile({"id": id_file})
    file.Trash()  # Mover a la papelera
    return {"message": "Archivo movido a la papelera"}


@router.post("/recover_file/{id_file}")
def recover_file(id_file: str):
    credentials = login()
    file = credentials.CreateFile({"id": id_file})
    file.UnTrash()  # Sacar de la papelera
    return {"message": "Archivo recuperado de la papelera"}


@router.delete("/delete_permanet/{id_file}")
def delete_permanent(id_file: str):
    credentials = login()
    file = credentials.CreateFile({"id": id_file})
    file.Delete()  # Eliminar permanentemente
    return {"message": "Archivo eliminado permanentemente"}


@router.post("/create_folder/")
def create_folder(folder_info: FolderInfo):
    credentials = login()
    folder = credentials.CreateFile(
        {
            "title": folder_info.folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [{"kind": "drive#fileLink", "id": folder_info.id_folder}]
            if folder_info.id_folder
            else [],
        }
    )
    folder.Upload()
    return {"message": "Carpeta creada exitosamente", "folder_id": folder["id"]}


@router.post("/move_file/")
def move_file(move_info: MoveInfo):
    credentials = login()
    file = credentials.CreateFile({"id": move_info.id_file})
    file["parents"] = [{"kind": "drive#fileLink", "id": move_info.id_folder}]
    file.Upload(param={"supportsTeamDrives": True})
    return {"message": "Archivo movido exitosamente"}


@router.get("/list_permissions/{id_drive}")
def list_permissions(id_drive: str):
    drive = login()
    file = drive.CreateFile({"id": id_drive})
    permissions = file.GetPermissions()
    return permissions


@router.post("/insert_permissions/")
def insert_permissions(permission_info: PermissionInfo):
    drive = login()
    file = drive.CreateFile({"id": permission_info.id_drive})
    permission = file.InsertPermission(
        {
            "type": permission_info.type,
            "value": permission_info.value,
            "role": permission_info.role,
        }
    )
    return {"message": "Permiso insertado exitosamente", "permission": permission}


@router.delete("/delete_permissions/{id_drive}")
def delete_permissions(
    id_drive: str, permission_id: Optional[str] = None, email: Optional[str] = None
):
    drive = login()
    file = drive.CreateFile({"id": id_drive})
    if permission_id:
        file.DeletePermission(permission_id)
    elif email:
        permissions = file.GetPermissions()
        for permission in permissions:
            if permission.get("emailAddress") == email:
                file.DeletePermission(permission["id"])
    else:
        raise HTTPException(status_code=400, detail="Se requiere permission_id o email")
    return {"message": "Permiso(s) eliminado(s) exitosamente"}
