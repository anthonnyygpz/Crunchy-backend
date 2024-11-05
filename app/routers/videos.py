from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv

from app.utils.logger_AWS.logger import logger
from app.utils.bucket_AWS.get_bucket import bucket_name, s3_client

from app.schemas.videos import VideoCreate, VideoResponse

load_dotenv()

router = APIRouter()


@router.get(
    "/videos/",
    response_model=dict,
    summary="Listar los videos.",
    description="Lista todo los video que hay almacenados.",
    tags=["videos"],
)
async def get_videos():
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", "")
        videos = [
            obj["Key"]
            for obj in response.get("Contents", [])
            if obj["Key"].endswith(video_extensions)
        ]
        logger.info(f"Lista de videos obtenida. Total: {len(videos)}")
        return JSONResponse(content={"videos": videos})
    except ClientError as e:
        logger.error(f"Error al listar videos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al listar videos")


@router.get(
    "/videos/{video_name}",
    response_model=VideoResponse,
    summary="Obtener la url.",
    description="Genera la url que mostrara la url del video.",
    tags=["videos"],
)
async def get_video(video_name: str):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=video_name)

        # Añadir parámetros para controlar el comportamiento de la descarga
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": video_name,
                "ResponseContentType": "video/mp4",  # Ajusta según el tipo de video
                "ResponseContentDisposition": "inline",  # Esto evita la descarga automática
            },
            ExpiresIn=172800,  # URL válida por 2 días
            HttpMethod="GET",
        )

        logger.info(f"URL generada para el video: {video_name}")
        return JSONResponse(
            content={"url": url},
            headers={
                "Content-Type": "application/json",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logger.warning(f"Video no encontrado: {video_name}")
            raise HTTPException(status_code=404, detail="Video no encontrado")
        logger.error(f"Error al generar URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al generar URL del video")
    except NoCredentialsError:
        logger.error("Credenciales de AWS no encontradas")
        raise HTTPException(
            status_code=500,
            detail="Error de configuración: Credenciales de AWS no encontradas",
        )


@router.post(
    "/videos/{video_name}",
    summary="Agregar metadatos.",
    description="En este apartado se agregaran los metadatos para ciertos parametros.",
    tags=["videos"],
)
async def add_metadata(video_name: str):
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=video_name)
        existing_metadata = response.get("Metadata", {})
        metadata = {
            "category": "educational",
            "subcategory": "programming",
            "language": "spanish",
            "duration": "10:30",
        }
        s3_client.copy_object(
            Bucket="crunchy-video",
            CopySource={"Bucket": bucket_name, "Key": video_name},
            Key="Fantastic places",
            Metadata={**existing_metadata, **metadata},
            MetadataDirective="REPLACE",
        )
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@router.post(
    "/videos/",
    response_model=dict,
    summary="Subir videos.",
    description="Almacenar videos para mostrar en la pagina web.",
    tags=[""],
)
async def create_video(video: VideoCreate):
    try:
        s3_client.upload_file(video.file_path, bucket_name, video.video_name)
        return {"Video": "Upload video successfully"}
    except NoCredentialsError:
        return {"Error": "Credentials not available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
