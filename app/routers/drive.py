from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

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

directorio_credenciales = "credentials_module.json"


def login():
    GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales


@router.get("/listar_contenido_carpeta/{folder_id}", response_model=List[FolderContent])
def listar_contenido_carpeta(folder_id: str):
    credenciales = login()
    query = f"'{folder_id}' in parents and trashed=false"
    lista_archivos = credenciales.ListFile({"q": query}).GetList()

    contenido = []
    for archivo in lista_archivos:
        contenido.append(
            FolderContent(
                id=archivo["id"],
                title=archivo["title"],
                mimeType=archivo["mimeType"],
                modifiedDate=archivo["modifiedDate"],
            )
        )

    return contenido


@router.post("/crear_archivo_texto/")
def crear_archivo_texto(file_info: FileInfo):
    credenciales = login()
    archivo = credenciales.CreateFile(
        {
            "title": file_info.nombre_archivo,
            "parents": [{"kind": "drive#fileLink", "id": file_info.id_folder}],
        }
    )
    archivo.SetContentString(file_info.contenido)
    archivo.Upload()
    return {"message": "Archivo creado exitosamente"}


@router.post("/subir_archivo/")
def subir_archivo(upload_info: UploadInfo):
    credenciales = login()
    archivo = credenciales.CreateFile(
        {"parents": [{"kind": "drive#fileLink", "id": upload_info.id_folder}]}
    )
    archivo["title"] = upload_info.ruta_archivo.split("/")[-1]
    archivo.SetContentFile(upload_info.ruta_archivo)
    archivo.Upload()
    return {"message": "Archivo subido exitosamente"}


@router.post("/bajar_archivo_por_id/")
def bajar_archivo_por_id(download_info: DownloadInfo):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": download_info.id_drive})
    nombre_archivo = archivo["title"]
    archivo.GetContentFile(download_info.ruta_descarga + nombre_archivo)
    return {"message": f"Archivo {nombre_archivo} descargado exitosamente"}


@router.post("/buscar/")
def buscar(search_query: SearchQuery):
    credenciales = login()
    lista_archivos = credenciales.ListFile({"q": search_query.query}).GetList()
    resultados = []
    for f in lista_archivos:
        resultados.append(
            {
                "ID Drive": f["id"],
                "Nombre del archivo": f["title"],
                "Tipo de archivo": f["mimeType"],
                "Fecha de creación": f["createdDate"],
                "Fecha de última modificación": f["modifiedDate"],
                "Tamaño": f["fileSize"],
            }
        )
    return resultados


@router.post("/borrar_archivo/{id_archivo}")
def borrar_archivo(id_archivo: str):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": id_archivo})
    archivo.Trash()  # Mover a la papelera
    return {"message": "Archivo movido a la papelera"}


@router.post("/recuperar_archivo/{id_archivo}")
def recuperar_archivo(id_archivo: str):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": id_archivo})
    archivo.UnTrash()  # Sacar de la papelera
    return {"message": "Archivo recuperado de la papelera"}


@router.delete("/eliminar_permanentemente/{id_archivo}")
def eliminar_permanentemente(id_archivo: str):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": id_archivo})
    archivo.Delete()  # Eliminar permanentemente
    return {"message": "Archivo eliminado permanentemente"}


@router.post("/crear_carpeta/")
def crear_carpeta(folder_info: FolderInfo):
    credenciales = login()
    folder = credenciales.CreateFile(
        {
            "title": folder_info.nombre_carpeta,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [{"kind": "drive#fileLink", "id": folder_info.id_folder}]
            if folder_info.id_folder
            else [],
        }
    )
    folder.Upload()
    return {"message": "Carpeta creada exitosamente", "folder_id": folder["id"]}


@router.post("/mover_archivo/")
def mover_archivo(move_info: MoveInfo):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": move_info.id_archivo})
    archivo["parents"] = [{"kind": "drive#fileLink", "id": move_info.id_folder}]
    archivo.Upload(param={"supportsTeamDrives": True})
    return {"message": "Archivo movido exitosamente"}


@router.get("/listar_permisos/{id_drive}")
def listar_permisos(id_drive: str):
    drive = login()
    file1 = drive.CreateFile({"id": id_drive})
    permisos = file1.GetPermissions()
    return permisos


@router.post("/insertar_permisos/")
def insertar_permisos(permission_info: PermissionInfo):
    drive = login()
    file1 = drive.CreateFile({"id": permission_info.id_drive})
    permission = file1.InsertPermission(
        {
            "type": permission_info.type,
            "value": permission_info.value,
            "role": permission_info.role,
        }
    )
    return {"message": "Permiso insertado exitosamente", "permission": permission}


@router.delete("/eliminar_permisos/{id_drive}")
def eliminar_permisos(
    id_drive: str, permission_id: Optional[str] = None, email: Optional[str] = None
):
    drive = login()
    file1 = drive.CreateFile({"id": id_drive})
    if permission_id:
        file1.DeletePermission(permission_id)
    elif email:
        permissions = file1.GetPermissions()
        for permiso in permissions:
            if permiso.get("emailAddress") == email:
                file1.DeletePermission(permiso["id"])
    else:
        raise HTTPException(status_code=400, detail="Se requiere permission_id o email")
    return {"message": "Permiso(s) eliminado(s) exitosamente"}
