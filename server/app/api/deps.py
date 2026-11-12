from typing import Generator

from sqlalchemy.orm import Session

from app.core.security import verify_api_key
from app.db.session import get_session

__all__ = ["get_db", "verify_api_key"]


def get_db() -> Generator[Session, None, None]:
    yield from get_session()
