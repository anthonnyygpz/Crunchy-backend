from fastapi import FastAPI
from app.routers import (
    videos,
    user_email_and_password_firebase_auth,
    playlist,
    token_firebase_auth,
)
from docs.documentation import configure_docs

app = FastAPI(title="Crunchy", version="1.0.0")

app.include_router(user_email_and_password_firebase_auth.router)
app.include_router(videos.router)
app.include_router(playlist.router)
app.include_router(token_firebase_auth.router)


configure_docs(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
