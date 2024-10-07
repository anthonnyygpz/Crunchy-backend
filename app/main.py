from fastapi import FastAPI
from app.routers import aws
from app.routers import firebaseAuth

app = FastAPI()

app.include_router(aws.router)
app.include_router(firebaseAuth.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
