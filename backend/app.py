import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from api.routers import client, manager
from core.config import Settings
from core.logger import log


app = FastAPI()
settings = Settings()

app.include_router(client.router, prefix="/client", tags=["Client"])
app.include_router(manager.router, prefix="/manager", tags=["Manager"])

origins = [
    "http://localhost.com",
    "https://localhost.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    log.info("Server started!")


@app.on_event("shutdown")
async def on_shutdown():
    log.info("Bye!")


@app.get("/")
async def root():
    return {"message": "Hello World"}


register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["models.client", "models.manager"]},
    generate_schemas=True
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
