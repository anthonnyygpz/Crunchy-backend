from pydantic import BaseModel, Field


class VideoResponse(BaseModel):
    video_name: str = Field(
        title="Nombre del video.",
        description="Aqui coloca el nombre del video que se desea ver.",
    )


class VideoCreate(BaseModel):
    file_path: str = Field(
        title="Directorio de local.",
        description="Aqui se coloca el directorio completo de donde se encuentra el video que se desea subir.",
    )
    video_name: str = Field(
        title="Nombre del video.",
        description="Aqui se coloca el nombre que se le dara al video.",
    )
