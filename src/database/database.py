from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base
from ..config import DATABASE_URL


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crea todas las tablas en la base de datos."""
    print("Inicializando la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada.")

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager para obtener una sesión de base de datos.
    Asegura que la sesión se cierre siempre después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    print("Creando la base de datos y las tablas si no existen...")
    init_db()
