# import requests
# import json
#
#
# def search_drive_files(query):
#     # URL de la API
#     url = "http://localhost:8000/search"  # Ajusta esta URL según donde esté alojada tu API
#
#     # Datos para enviar en la solicitud POST
#     data = {"query": query}
#
#     # Cabeceras para especificar que estamos enviando JSON
#     headers = {"Content-Type": "application/json"}
#
#     try:
#         # Realizar la solicitud POST
#         response = requests.post(url, data=json.dumps(data), headers=headers)
#
#         # Verificar si la solicitud fue exitosa
#         if response.status_code == 200:
#             # Parsear la respuesta JSON
#             results = response.json()
#             print("Resultados de la búsqueda:")
#             for file in results["results"]:
#                 print(f"Título: {file['title']}, ID: {file['id']}")
#         else:
#             print(f"Error en la solicitud: {response.status_code}")
#             print(response.text)
#
#     except requests.exceptions.RequestException as e:
#         print(f"Error al realizar la solicitud: {e}")
#
#
# # Uso de la función
# search_query = input("Ingrese el término de búsqueda: ")
# search_drive_files(search_query)
# import requests
#
# def edit_folder_name(base_url, folder_id, new_name):
#     endpoint = f"{base_url}/edit_folder/{folder_id}"
#
#     data = {"new_name": new_name}
#
#     try:
#         response = requests.put(endpoint, params=data)
#
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return f"Error: {response.status_code} - {response.text}"
#
#     except requests.RequestException as e:
#         return f"Error de conexión: {str(e)}"
#
# if __name__ == "__main__":
#     BASE_URL = "http://localhost:8000"  # Asegúrate de que esta URL coincida con donde está corriendo tu API
#     FOLDER_ID = "1O-BixiYiVYXa6Dch0fo6DaVeyxiAbL5b"  # Reemplaza con el ID de la carpeta que quieres editar
#     NEW_NAME = "Funciono"
#
#     result = edit_folder_name(BASE_URL, FOLDER_ID, NEW_NAME)
#     print(result)


# import requests
#
#
# def delete_folder(base_url, folder_id):
#     endpoint = f"{base_url}/delete_file_or_folder/{folder_id}"
#
#     try:
#         response = requests.delete(endpoint)
#
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return f"Error: {response.status_code} - {response.text}"
#
#     except requests.RequestException as e:
#         return f"Error de conexión: {str(e)}"
#
#
# if __name__ == "__main__":
#     BASE_URL = "http://localhost:8000"  # Asegúrate de que esta URL coincida con donde está corriendo tu API
#     FOLDER_ID = "1-PyzZDqOy22HY1mhqdAXxHmdBeCe3Rf5"  # Reemplaza con el ID de la carpeta que quieres editar
#     # NEW_NAME = "Funciono"
#
#     result = delete_folder(BASE_URL, FOLDER_ID)
#     print(result)
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError

directorio_credenciales = "credentials_module.json"


# INICIAR SESION
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


def busca(query):
    resultado = []
    credenciales = login()
    # Archivos con el nombre 'mooncode': title = 'mooncode'
    # Archivos que contengan 'mooncode' y 'mooncoders': title contains 'mooncode' and title contains 'mooncoders'
    # Archivos que NO contengan 'mooncode': not title contains 'mooncode'
    # Archivos que contengan 'mooncode' dentro del archivo: fullText contains 'mooncode'
    # Archivos en el basurero: trashed=true
    # Archivos que se llamen 'mooncode' y no esten en el basurero: title = 'mooncode' and trashed = false
    lista_archivos = credenciales.ListFile({"q": query}).GetList()
    for f in lista_archivos:
        # ID Drive
        print("ID Drive:", f["id"])
        # Link de visualizacion embebido
        print("Link de visualizacion embebido:", f["embedLink"])
        # Link de descarga
        print("Link de descarga:", f["downloadUrl"])
        # Nombre del archivo
        print("Nombre del archivo:", f["title"])
        # Tipo de archivo
        print("Tipo de archivo:", f["mimeType"])
        # Esta en el basurero
        print("Esta en el basurero:", f["labels"]["trashed"])
        # Fecha de creacion
        print("Fecha de creacion:", f["createdDate"])
        # Fecha de ultima modificacion
        print("Fecha de ultima modificacion:", f["modifiedDate"])
        # Version
        print("Version:", f["version"])
        # Tamanio
        print("Tamanio:", f["fileSize"])
        resultado.append(f)

    return resultado
