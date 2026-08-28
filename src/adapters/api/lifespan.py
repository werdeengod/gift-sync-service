import logging
from typing import TYPE_CHECKING
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from src.bootstrap import build_container

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: 'FastAPI'):
    logger.info("Starting application")

    container = build_container()
    setup_dishka(container, app)

    logger.info("Application started")

    yield

    await container.close()

    logger.info("Shutdown complete")
