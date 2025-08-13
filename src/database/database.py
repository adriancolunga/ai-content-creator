from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base
from ..config import DATABASE_URL

# El engine es el punto de entrada a la base de datos.
# connect_args es específico para SQLite para permitir operaciones en múltiples hilos.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# SessionLocal es una fábrica de sesiones. Las instancias de esta clase
# representarán una conexión transaccional a la BD.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crea todas las tablas en la base de datos."""
    print("Inicializando la base de datos...")
    # La siguiente línea crea las tablas definidas en models.py
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada.")

# --- Dependency for using sessions in the application ---
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
    # Este script se puede ejecutar para crear la base de datos inicial.
    print("Creando la base de datos y las tablas si no existen...")
    init_db()
