# db.py
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from settings.settings import settings

class Base(DeclarativeBase):
    pass

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,          # evita conexiones muertas
    # pool_size=10, max_overflow=20, pool_timeout=30,  # ajústalo según carga
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,      # útil si commiteás acá
    class_=Session,
)

def get_db() -> Generator[Session, None, None]:
    """
    Crea una sesión por request. Si no hubo excepción, hace commit.
    Si hubo, rollback y re-lanza para que FastAPI devuelva el error correcto.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
