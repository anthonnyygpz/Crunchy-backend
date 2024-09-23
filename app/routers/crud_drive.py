from typing import List

from fastapi import APIRouter, HTTPException, applications
from fastapi.exceptions import RequestErrorModel
from google.auth.exceptions import GoogleAuthError
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError

from app.schemas.crud_drive import FolderContent, FolderInfo
from app.schemas.drive import FileInfo

router = APIRouter()

credentials_directory = "credentials_module.json"


def login():
    GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = credentials_directory
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_directory)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(credentials_directory)
    credentials = GoogleDrive(gauth)
    return credentials


# CRUD Folder
@router.post("/create_folder/")
def create_folder(folder_info: FolderInfo):
    try:
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
        results = [
            {"message": "Carpeta creada exitosamente", "folder_id": folder["id"]}
        ]
        return {"results": results}
    except ApiRequestError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear la carpeta: {str(e)}"
        )


@router.post("/foldes/", response_model=List[FolderContent])
def list_folder_contents():
    try:
        credentials = login()
        query = "mimeType='application/vnd.google-apps.folder' and trashed=false"
        file_list = credentials.ListFile({"q": query}).GetList()

        content = [
            FolderContent(id=file["id"], title=file["title"]) for file in file_list
        ]
        return content
    except ApiRequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar las carpetas: {str(e)}",
        )


@router.post("/sub_folders/{folder_id}", response_model=List[FolderContent])
def sub_folders(folder_id: str):
    try:
        credentials = login()
        folder = credentials.CreateFile({"id": folder_id})
        folder.FetchMetadata()

        if folder["mimeType"] != "application/vnd.google-apps.folder":
            raise HTTPException(
                status_code=400,
                detail="El ID proporcionado no corresponde a una carpeta",
            )

        query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        file_list = credentials.ListFile({"q": query}).GetList()

        subfolders = [
            FolderContent(id=file["id"], title=file["title"]) for file in file_list
        ]
        return subfolders
    except ApiRequestError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al obtener las lista de carpetas: {str(e)}",
        )


@router.put("/edit_folder/{folder_id}")
def edit_folder(folder_id: str, new_name: str):
    try:
        credentials = login()
        folder = credentials.CreateFile({"id": folder_id})

        try:
            folder.FetchMetadata()
        except ApiRequestError:
            raise HTTPException(status_code=404, detail="Carpeta no encontrada")

        if folder["mimeType"] != "application/vnd.google-apps.folder":
            raise HTTPException(
                status_code=400,
                detail="El ID proporcionado no corresponde a una carpeta",
            )

        folder["title"] = new_name
        folder.Upload()

        return {"message": f"Carpeta actualizada con éxito. Nuevo nombre: {new_name}"}
    except ApiRequestError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar la carpeta: {str(e)}",
        )


@router.delete("/delete/{id}")
def delete_file_or_folder(id: str):
    try:
        credentials = login()
        folder_or_file = credentials.CreateFile({"id": id})
        folder_or_file.Trash()
        return {"message": "Archivo movido a la papelera"}
    except ApiRequestError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al borrar borrar una carpeta o archivo: {str(e)}",
        )


# CRUD file
# @router.post("/create_file/")
# def create_file(file_info: FileInfo):
#     try:
#         credentials = login()
#         file = credentials.CreateFile(
#             {
#                 "title": file_info.file_name,
#                 "parents": [{"kind": "drive#fileLink", "id": file_info.id_folder}],
#             }
#         )
#         file.SetContentFile(file_info.content)
#         file.Upload()
#         return {"message": "Archivo creado exitosamente"}
#     except ApiRequestError as e:
#         raise HTTPException(
#             status_code=400, detail=f"Error al crear el archivo: {str(e)}"
#         )


@router.post("/list_file/", response_model=FileInfo)
def list_file():
    try:
        credentials = login()
        file_list = credentials.ListFile({
            
        })
        
    except ApiRequestError as e:
        raise HTTPException(status_code=400, detail=f"Error al listar los archivos: {str(e)}")
