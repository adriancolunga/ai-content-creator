from sqlalchemy.orm import Session
from ..database.models import Idea
from ..database.database import get_db
from typing import Optional

def get_next_pending_idea() -> Optional[Idea]:
    """
    Busca la primera idea pendiente de la base de datos, la marca como 'processing'
    para evitar que otro proceso la tome (bloqueo a nivel de fila), y la devuelve.

    Returns:
        La entidad Idea si se encuentra una pendiente, de lo contrario None.
    """
    try:
        with get_db() as db:
            idea = db.query(Idea).filter(Idea.status == 'pending').order_by(Idea.created_at.asc()).with_for_update().first()
            
            if idea:
                print(f"Idea ID {idea.id} seleccionada. Cambiando estado a 'processing'.")
                idea.status = 'processing'
                db.commit()
                db.refresh(idea)
                return idea
            return None
    except Exception as e:
        print(f"Error al obtener la siguiente idea: {e}")
        return None

def update_idea_status(idea_id: int, status: str, error_message: str = None):
    """Actualiza el estado de una idea."""
    try:
        with get_db() as db:
            idea = db.query(Idea).filter(Idea.id == idea_id).first()
            if idea:
                idea.status = status
                if error_message:
                    print(f"Error en idea {idea_id}: {error_message}")
                db.commit()
                print(f"Idea ID {idea.id} actualizada a estado '{status}'.")
    except Exception as e:
        print(f"Error al actualizar el estado de la idea {idea_id}: {e}")
