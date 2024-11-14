from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import movies, user
from docs.documentation import configure_docs

app = FastAPI(title="Crunchy", version="1.0.0")

app.include_router(user.router)
app.include_router(movies.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configure_docs(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=10000)
