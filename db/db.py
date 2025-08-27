# db.py
from contextlib import contextmanager
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

@contextmanager
def session_scope() -> Session:
    """Crea una sesión y maneja commit/rollback automáticamente."""
    db = SessionLocal()
    try:
        yield db           # aquí entregamos la sesión al bloque with
        db.commit()        # si no hubo excepción -> commit
    except:
        db.rollback()      # si hubo excepción -> rollback
        raise
    finally:
        db.close()         # siempre cerramos la sesión

def create_tables():
    Base.metadata.create_all(bind=engine)
