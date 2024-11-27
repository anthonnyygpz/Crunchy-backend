from fastapi import HTTPException
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import cv2

from app.crud.crud_movies import MovieDB
from app.schemas.movies import MovieUploadData
from app.utils.bucket_AWS.get_bucket import bucket_name, s3_client
from app.utils.logger_AWS.logger import logger


class MovieServiceDB:
    def __init__(self, db: Session):
        self.db = db

    def uploads(self, movie: MovieUploadData, file_path: str):
        try:
            video = cv2.VideoCapture(file_path)
            total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = video.get(cv2.CAP_PROP_FPS)
            duration = int(total_frames / fps)
            video.release()

            s3_client.upload_file(file_path, bucket_name, movie.title)
            MovieDB(self.db).upload_movie_data(movie, duration)
            return {"Video": "Upload video successfully"}
        except NoCredentialsError:
            return {"Error": "Credentials not available"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def get_videos_name(self, skip: int, limit: int):
        try:
            movie_name = MovieDB(self.db).get_movie_name(skip, limit)
            return movie_name
        except ClientError as e:
            logger.error(f"Error al listar videos: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al listar videos")

    def generate_urls(self, video_name: str):
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
            raise HTTPException(
                status_code=500, detail="Error al generar URL del video"
            )
        except NoCredentialsError:
            logger.error("Credenciales de AWS no encontradas")
            raise HTTPException(
                status_code=500,
                detail="Error de configuración: Credenciales de AWS no encontradas",
            )

    def details_movie(self, title: str):
        title_movie = MovieDB(self.db).details_movie(title)
        if not title_movie:
            return {"message": "title movie not exits"}
        return title_movie
