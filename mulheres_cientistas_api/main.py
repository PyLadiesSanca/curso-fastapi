from contextlib import asynccontextmanager

from fastapi import FastAPI

from mulheres_cientistas_api.database import init_db
from mulheres_cientistas_api.routers import cientista, frase


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="API de Mulheres Cientistas",
    lifespan=lifespan
)
app.include_router(cientista.router)
app.include_router(frase.router)


@app.get("/")
def index():
    return {"title": "API de Mulheres Cientistas"}
