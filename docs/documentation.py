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
                "name": "videos",
                "description": "Operaciones con videos",
            },
        ]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
