import time
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from src.agents.graph import get_graph
from src.database.database import init_db
from src.config import check_env_vars
from src.logic.idea_manager import get_next_pending_idea, update_idea_status

def main():
    """Punto de entrada principal del servicio de automatización."""
    try:
        check_env_vars()
        print("Variables de entorno verificadas.")
    except ValueError as e:
        print(f"Error de configuración: {e}")
        return

    init_db()
    
    print("Iniciando el servicio de automatización. Presiona Ctrl+C para salir.")

if __name__ == "__main__":
    main()
