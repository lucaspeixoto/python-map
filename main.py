from fastapi import FastAPI
from app.db import database
from app.models import user as user_model
from app.routers import user as user_router, map

user_model.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user_router.router)
app.include_router(map.router)

@app.get("/")
def home():
    return {"mensagem": "API está funcionando!"}