import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator


DATABASE_URL = (
    os.environ.get("DATABASE_URL")
    or os.environ.get("SQLITE_FILE")
    or "sqlite:///./iot_enrichment.db"
)


engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a SQLModel Session for dependency injection."""
    with Session(engine) as session:
        yield session


def init_admin_user(admin_password: str | None = None) -> None:
    """Create the admin user if it doesn't exist.

    The admin password is taken from the ADMIN_PASSWORD environment variable
    if not provided.
    """
    from app.auth import get_password_hash
    from app.crud import get_user_by_username, create_user
    from app.models import User

    if admin_password is None:
        admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_password:
        return

    init_db()
    with Session(engine) as session:
        existing = get_user_by_username(session, "admin")
        if existing:
            return
        user = User(
            username="admin",
            hashed_password=get_password_hash(admin_password),
            is_admin=True,
        )
        create_user(session, user)
