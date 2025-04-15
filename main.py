from fastapi import FastAPI
from app.db import database, models
from app.routers import user

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def home():
    return {"mensagem": "API está funcionando!"}
