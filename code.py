import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"


def crear_archivo_texto(nombre_archivo: str, contenido: str, id_folder: str):
    url = f"{BASE_URL}/crear_archivo_texto/"
    data = {
        "nombre_archivo": nombre_archivo,
        "contenido": contenido,
        "id_folder": id_folder,
    }
    response = requests.post(url, json=data)
    return response.json()


def subir_archivo(ruta_archivo: str, id_folder: str):
    url = f"{BASE_URL}/subir_archivo/"
    data = {"ruta_archivo": ruta_archivo, "id_folder": id_folder}
    response = requests.post(url, json=data)
    return response.json()


def bajar_archivo_por_id(id_drive: str, ruta_descarga: str):
    url = f"{BASE_URL}/bajar_archivo_por_id/"
    data = {"id_drive": id_drive, "ruta_descarga": ruta_descarga}
    response = requests.post(url, json=data)
    return response.json()


def buscar(query: str):
    url = f"{BASE_URL}/buscar/"
    data = {"query": query}
    response = requests.post(url, json=data)
    return response.json()


def borrar_archivo(id_archivo: str):
    url = f"{BASE_URL}/borrar_archivo/{id_archivo}"
    response = requests.post(url)
    return response.json()


def recuperar_archivo(id_archivo: str):
    url = f"{BASE_URL}/recuperar_archivo/{id_archivo}"
    response = requests.post(url)
    return response.json()


def eliminar_permanentemente(id_archivo: str):
    url = f"{BASE_URL}/eliminar_permanentemente/{id_archivo}"
    response = requests.delete(url)
    return response.json()


def crear_carpeta(nombre_carpeta: str, id_folder: Optional[str] = None):
    url = f"{BASE_URL}/crear_carpeta/"
    data = {"nombre_carpeta": nombre_carpeta, "id_folder": id_folder}
    response = requests.post(url, json=data)
    return response.json()


def mover_archivo(id_archivo: str, id_folder: str):
    url = f"{BASE_URL}/mover_archivo/"
    data = {"id_archivo": id_archivo, "id_folder": id_folder}
    response = requests.post(url, json=data)
    return response.json()


def listar_permisos(id_drive: str):
    url = f"{BASE_URL}/listar_permisos/{id_drive}"
    response = requests.get(url)
    return response.json()


def insertar_permisos(id_drive: str, type: str, value: str, role: str):
    url = f"{BASE_URL}/insertar_permisos/"
    data = {"id_drive": id_drive, "type": type, "value": value, "role": role}
    response = requests.post(url, json=data)
    return response.json()


def eliminar_permisos(
    id_drive: str, permission_id: Optional[str] = None, email: Optional[str] = None
):
    url = f"{BASE_URL}/eliminar_permisos/{id_drive}"
    params = {}
    if permission_id:
        params["permission_id"] = permission_id
    if email:
        params["email"] = email
    response = requests.delete(url, params=params)
    return response.json()


def listar_contenido_carpeta(folder_id: str):
    url = f"{BASE_URL}/listar_contenido_carpeta/{folder_id}"
    response = requests.get(url)
    return response.json()


def main():
    while True:
        print("\n--- Google Drive API Client ---")
        print("1. Crear archivo de texto")
        print("2. Subir archivo")
        print("3. Descargar archivo")
        print("4. Buscar archivos")
        print("5. Borrar archivo (mover a papelera)")
        print("6. Recuperar archivo de papelera")
        print("7. Eliminar archivo permanentemente")
        print("8. Crear carpeta")
        print("9. Mover archivo")
        print("10. Listar permisos")
        print("11. Insertar permisos")
        print("12. Eliminar permisos")
        print("0. Salir")

        choice = input("Seleccione una opción: ")

        match choice:
            case "1":
                nombre_archivo = input("Nombre del archivo: ")
                contenido = input("Contenido del archivo: ")
                id_folder = input("ID de la carpeta: ")
                print(crear_archivo_texto(nombre_archivo, contenido, id_folder))

            case "2":
                ruta_archivo = input("Ruta del archivo: ")
                id_folder = input("ID de la carpeta: ")
                print(subir_archivo(ruta_archivo, id_folder))

            case "3":
                id_drive = input("ID del archivo: ")
                ruta_descarga = input("Ruta de descarga: ")
                print(bajar_archivo_por_id(id_drive, ruta_descarga))

            case "4":
                query = input("Query de búsqueda: ")
                print(json.dumps(buscar(query), indent=2))

            case "5":
                id_archivo = input("ID del archivo: ")
                print(borrar_archivo(id_archivo))

            case "6":
                id_archivo = input("ID del archivo: ")
                print(recuperar_archivo(id_archivo))

            case "7":
                id_archivo = input("ID del archivo: ")
                print(eliminar_permanentemente(id_archivo))

            case "8":
                nombre_carpeta = input("Nombre de la carpeta: ")
                id_folder = input("ID de la carpeta padre (opcional): ")
                print(crear_carpeta(nombre_carpeta, id_folder if id_folder else None))

            case "9":
                id_archivo = input("ID del archivo: ")
                id_folder = input("ID de la carpeta destino: ")
                print(mover_archivo(id_archivo, id_folder))

            case "10":
                id_drive = input("ID del archivo: ")
                print(json.dumps(listar_permisos(id_drive), indent=2))

            case "11":
                id_drive = input("ID del archivo: ")
                type = input("Tipo de permiso (anyone/group/user): ")
                value = input("Valor (email): ")
                role = input("Rol (owner/writer/reader): ")
                print(insertar_permisos(id_drive, type, value, role))

            case "12":
                id_drive = input("ID del archivo: ")
                choice = input("Eliminar por ID de permiso (1) o por email (2)? ")
                if choice == "1":
                    permission_id = input("ID del permiso: ")
                    print(eliminar_permisos(id_drive, permission_id=permission_id))
                elif choice == "2":
                    email = input("Email: ")
                    print(eliminar_permisos(id_drive, email=email))
                else:
                    print("Opción no válida")

            case "13":
                folder_id = input("ID de la carpeta: ")
                contenido = listar_contenido_carpeta(folder_id)
                print("\nContenido de la carpeta:")
                for item in contenido:
                    print(f"ID: {item['id']}")
                    print(f"Nombre: {item['title']}")
                    print(f"Tipo: {item['mimeType']}")
                    print(f"Última modificación: {item['modifiedDate']}")
                    print("---")

            case "0":
                print("¡Hasta luego!")
                break

            case _:
                print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    main()
