from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import logging
import boto3
import os

from app.schemas.videos import VideoRequest, UploadVideo

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

router = APIRouter()


def get_bucket_region(bucket_name):
    s3_client = boto3.client("s3")
    try:
        location = s3_client.get_bucket_location(Bucket=bucket_name)
        return location["LocationConstraint"] or "us-east-1"
    except ClientError as e:
        logger.error(f"Error al obtener la región del bucket: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error al obtener la región del bucket"
        )


# Configuración de AWS con firma v4
bucket_name = os.getenv("S3_BUCKET_NAME")
region = get_bucket_region(bucket_name)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=region,
    config=Config(signature_version="s3v4"),
)


@router.post("/upload/")
async def upload_video(upload: UploadVideo):
    try:
        s3_client.upload_file(upload.filepath, bucket_name, upload.videoName)
        return {"Video": "Upload video successfully"}
    except NoCredentialsError:
        return {"Error": "Credentials not available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/get-video-url")
async def get_video_url(request: VideoRequest):
    try:
        # Verificar si el archivo existe
        s3_client.head_object(Bucket=bucket_name, Key=request.video_key)

        # Generar URL prefirmada con firma v4
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": request.video_key},
            # ExpiresIn=3600,  # URL válida por 1 hora
            HttpMethod="GET",
        )
        logger.info(f"URL generada para el video: {request.video_key}")
        return JSONResponse(content={"url": url})
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logger.warning(f"Video no encontrado: {request.video_key}")
            raise HTTPException(status_code=404, detail="Video no encontrado")
        logger.error(f"Error al generar URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al generar URL del video")
    except NoCredentialsError:
        logger.error("Credenciales de AWS no encontradas")
        raise HTTPException(
            status_code=500,
            detail="Error de configuración: Credenciales de AWS no encontradas",
        )


@router.get("/list-videos")
async def list_videos():
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        videos = [
            obj["Key"]
            for obj in response.get("Contents", [])
            if obj["Key"].endswith((".mp4", ".avi", ".mov", ".webm", ""))
        ]
        logger.info(f"Lista de videos obtenida. Total: {len(videos)}")
        return JSONResponse(content={"videos": videos})
    except ClientError as e:
        logger.error(f"Error al listar videos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al listar videos")
