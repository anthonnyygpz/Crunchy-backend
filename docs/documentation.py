from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI


def configure_docs(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Personalizar documentación por módulos
        openapi_schema["tags"] = [
            {
                "name": "users",
                "description": "Operaciones con usuarios",
            },
            {
                "name": "movies",
                "description": "Operaciones con peliculas",
            },
            {
                "name": "watch_later",
                "description": "Operaciones con ver mas tarde",
            },
            {
                "name": "categories",
                "description": "Operaciones con categorias",
            },
            {
                "name": "history",
                "description": "Operaciones con historial",
            },
        ]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
