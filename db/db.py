# db.py
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from settings.settings import settings

class Base(DeclarativeBase):
    pass

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, 
    pool_recycle=3600
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
    """Crea una sesión y maneja commit/rollback automáticamente."""
    db = SessionLocal()
    try:
        yield db           # aquí entregamos la sesión al bloque with
    except:
        db.rollback()      # si hubo excepción -> rollback
        raise
    finally:
        db.close()         # siempre cerramos la sesión

def create_tables():
    Base.metadata.create_all(bind=engine)
