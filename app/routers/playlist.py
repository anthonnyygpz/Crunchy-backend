from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from mysql.connector import Error
from datetime import datetime
import time

from app.db.mysql import mydb
from app.schemas.playlist import CreatePlaylist

load_dotenv()

router = APIRouter()
mycursor = mydb.cursor()

timeStamp = datetime.fromtimestamp(time.time())


@router.post(
    "/playlists/",
    summary="Crear lista de reproduccion",
    description="Create playlist of the user",
)
async def create_playlist(create_playlist: CreatePlaylist):
    try:
        query = "INSERT INTO Playlist(createdAt,createdBy,isPlublic,thumbnailUrl,title,updatedAt,videoCount,videoId) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
        data = (
            timeStamp,
            create_playlist.createdBy,
            create_playlist.isPublic,
            create_playlist.tumbnailUrl,
            create_playlist.title,
            timeStamp,
            create_playlist.videoCount,
            create_playlist.videoId,
        )
        mycursor.execute(query, data)
        mydb.commit()
        return {"playlist": "Playlist created successfully"}
    except Error as e:
        raise HTTPException(status_code=400, detail=f"Error while creating: {str(e)}")


@router.get("/playlist/{id_playlist}")
async def get_playlist(id_playlist: str):
    try:
        query = "SELECT * FROM Playlist WHERE IDplaylist = %s"
        data = [id_playlist]
        mycursor.execute(query, data)
        result = mycursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=400, detail=f"Error while getting: {str(e)}")


@router.get("/playlist/")
async def get_playlists():
    try:
        query = "SELECT * FROM Playlist"
        mycursor.execute(query)
        result = mycursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=400, detail=f"Error while getting: {str(e)}")


# @router.put("/playlist/{id_playlist}")
# async def update_playlist(id_playlist: str):
#     try:
#         query = "UPDATE Playlist SET "
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error while updating: {str(e)}")


@router.delete("/playlist/{id_playlist}")
async def delete_playlist(id_playlist: str):
    try:
        query = "DELETE FROM Playlist WHERE IDplaylist = %s"
        data = [id_playlist]
        mycursor.execute(query, data)
        return {"playlist": "Playlist deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=400, detail=f"Error while deleting: {str(e)}")
