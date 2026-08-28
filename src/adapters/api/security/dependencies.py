from typing import Annotated
import logging
from fastapi import Header, Depends, HTTPException

from src.config import config
from src.domain.entities import User
from .jwt_service import JWTService


logger = logging.getLogger(__name__)


def get_jwt_service():
    return JWTService(
        secret_key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )


async def get_current_user(
    authorization: Annotated[str, Header(...)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)]
):
    if not authorization.startswith("Bearer "):
        logger.warning(f"Auth failed: {authorization[:20]}...")
        raise HTTPException(
            status_code=401,
            detail="Only Bearer token allowed"
        )

    token = authorization.split(" ")[1]
    payload = jwt_service.verify_token(token)

    logger.info(f"User {payload.user_id} authorized")

    return payload


CurrentUser = Annotated[User, Depends(get_current_user)]
