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
    tags=["aws"],
)
async def get_videos():
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        videos = [
            obj["Key"]
            for obj in response.get("Contents", [])
            if obj["Key"].endswith(("*"))
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
    tags=["aws"],
)
async def get_video(video_name: str):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=video_name)

        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": video_name},
            # ExpiresIn=3600,  # URL válida por 1 hora
            HttpMethod="GET",
        )
        logger.info(f"URL generada para el video: {video_name}")
        return JSONResponse(content={"url": url})
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
    "/videos/",
    response_model=dict,
    summary="Subir videos.",
    description="Almacenar videos para mostrar en la pagina web.",
    tags=["aws"],
)
async def create_video(video: VideoCreate):
    try:
        s3_client.upload_file(video.file_path, bucket_name, video.video_name)
        return {"Video": "Upload video successfully"}
    except NoCredentialsError:
        return {"Error": "Credentials not available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
