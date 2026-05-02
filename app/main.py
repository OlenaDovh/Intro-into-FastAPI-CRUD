from fastapi import FastAPI
from app.routers import items

app = FastAPI(title="FastAPI CRUD Demo")

app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI CRUD"}