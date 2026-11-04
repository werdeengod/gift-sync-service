import uvicorn
from fastapi import FastAPI

from src.config import config
from .routers import gifts
from .lifespan import lifespan


def create_app():
    fastapi = FastAPI(
        title="Gifts API",
        version="1.0.0",
        description="API for managing gifts",
        lifespan=lifespan
    )

    fastapi.include_router(gifts.router)

    return fastapi


if __name__ == '__main__':
    app = create_app()

    uvicorn.run(
        app,
        host='0.0.0.0',
        port='8000',
        reload=config.DEBUG,
        log_level='info',
    )
