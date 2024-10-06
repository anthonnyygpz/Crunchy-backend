from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import logging
import boto3
import os

from app.schemas.aws import VideoRequest

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


@router.post("/get-video-url")
async def get_video_url(request: VideoRequest):
    try:
        # Verificar si el archivo existe
        s3_client.head_object(Bucket=bucket_name, Key=request.video_key)

        # Generar URL prefirmada con firma v4
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": request.video_key},
            ExpiresIn=3600,  # URL válida por 1 hora
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
            if obj["Key"].endswith((".mp4", ".avi", ".mov"))
        ]
        logger.info(f"Lista de videos obtenida. Total: {len(videos)}")
        return JSONResponse(content={"videos": videos})
    except ClientError as e:
        logger.error(f"Error al listar videos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al listar videos")


# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(router, host="0.0.0.0", port=8000)


# from fastapi import APIRouter, HTTPException, Request
# from fastapi.responses import StreamingResponse, HTMLResponse
# import boto3
# from botocore.exceptions import ClientError
# from dotenv import load_dotenv
# import os
#
# router = APIRouter()
#
#
# load_dotenv()
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# REGION_NAME = os.getenv("REGION_NAME")
#
# # Configura el cliente de S3
# s3 = boto3.client(
#     "s3",
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#     region_name=REGION_NAME,
# )
#
#
# @router.get("/video/{video_name}")
# async def get_video(video_name: str):
#     bucket_name = "crunchy-video"
#
#     try:
#         file = s3.get_object(Bucket=bucket_name, Key=video_name)
#
#         def iterfile():
#             yield from file["Body"].iter_chunks()
#
#         return StreamingResponse(iterfile(), media_type="video/mp4")
#
#     except ClientError as e:
#         if e.response["Error"]["Code"] == "NoSuchKey":
#             raise HTTPException(status_code=404, detail="Video no encontrado")
#         else:
#             raise HTTPException(status_code=500, detail="Error al acceder al video")
#
#
# @router.get("/watch/{video_name}", response_class=HTMLResponse)
# async def watch_video(request: Request, video_name: str):
#     video_url = f"/video/{video_name}"
#
#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="es">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Ver Video: {video_name}</title>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 height: 100vh;
#                 margin: 0;
#                 background-color: #f0f0f0;
#             }}
#             .video-container {{
#                 max-width: 800px;
#                 width: 100%;
#                 box-shadow: 0 0 10px rgba(0,0,0,0.1);
#                 position: relative;
#             }}
#             video {{
#                 width: 100%;
#                 height: auto;
#             }}
#             #customPlayPause {{
#                 position: absolute;
#                 bottom: 20px;
#                 left: 20px;
#                 background-color: rgba(0, 0, 0, 0.7);
#                 color: white;
#                 border: none;
#                 border-radius: 50%;
#                 width: 50px;
#                 height: 50px;
#                 font-size: 20px;
#                 cursor: pointer;
#                 transition: background-color 0.3s;
#             }}
#             #customPlayPause:hover {{
#                 background-color: rgba(0, 0, 0, 0.9);
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="video-container">
#             <video id="myVideo">
#                 <source src="{video_url}" type="video/mp4">
#                 Tu navegador no soporta el elemento de video.
#             </video>
#             <button id="customPlayPause">▶</button>
#         </div>
#         <script>
#             const video = document.getElementById('myVideo');
#             const playPauseButton = document.getElementById('customPlayPause');
#
#             playPauseButton.addEventListener('click', () => {{
#                 if (video.paused) {{
#                     video.play();
#                     playPauseButton.textContent = '⏸';
#                 }} else {{
#                     video.pause();
#                     playPauseButton.textContent = '▶';
#                 }}
#             }});
#
#             video.addEventListener('play', () => {{
#                 playPauseButton.textContent = '⏸';
#             }});
#
#             video.addEventListener('pause', () => {{
#                 playPauseButton.textContent = '▶';
#             }});
#         </script>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)
