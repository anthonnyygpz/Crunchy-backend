from fastapi import FastAPI
from app.routers import videos
from app.routers import firebaseAuth
from app.routers import playlist

app = FastAPI(openapi_url="/openapi.json/")

app.include_router(videos.router)
app.include_router(firebaseAuth.router)
app.include_router(playlist.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
