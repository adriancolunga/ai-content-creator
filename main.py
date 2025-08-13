import time
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from src.agents.graph import get_graph
from src.database.database import init_db
from src.config import check_env_vars
from src.logic.idea_manager import get_next_pending_idea, update_idea_status

def run_pipeline(idea_text: str, idea_id: int):
    """
    Ejecuta el pipeline completo de generación de video para una idea dada.
    """
    print(f"\n--- Iniciando pipeline para la idea ID {idea_id}: '{idea_text}' ---")
    app = get_graph()

    initial_state = {
        "idea": idea_text,
        "project_id": None, # Se asignará en el primer nodo
        "retries": 0
    }

    final_state = None
    try:
        # Invocar el grafo con el estado inicial
        for s in app.stream(initial_state):
            node_name = list(s.keys())[0]
            print(f"    - Nodo completado: {node_name}")
            final_state = list(s.values())[0]

        if final_state and final_state.get("error"):
            raise Exception(final_state.get("error"))

        print(f"--- Pipeline finalizado con éxito para la idea ID {idea_id} ---")
        update_idea_status(idea_id, 'completed')

    except Exception as e:
        print(f"!!! Error en el pipeline para la idea ID {idea_id}: {e} !!!")
        update_idea_status(idea_id, 'failed', error_message=str(e))


def pipeline_job():
    """
    La función de trabajo que el scheduler ejecutará periódicamente.
    Busca una idea pendiente y, si la encuentra, ejecuta el pipeline.
    """
    print(f"\n[{time.ctime()}] Scheduler activado. Buscando nueva idea...")
    idea = get_next_pending_idea()
    
    if idea:
        run_pipeline(idea.text, idea.id)
    else:
        print(f"[{time.ctime()}] No hay ideas pendientes. Esperando al próximo ciclo.")


def main():
    """Punto de entrada principal del servicio de automatización."""
    # 1. Verificar configuración
    try:
        check_env_vars()
        print("Variables de entorno verificadas.")
    except ValueError as e:
        print(f"Error de configuración: {e}")
        return

    # 2. Inicializar la base de datos y crear tablas si no existen
    init_db()

    # 3. Configurar y lanzar el scheduler
    scheduler = BlockingScheduler(timezone="UTC")
    # Ejecuta el job cada 5 minutos (puedes ajustarlo a 'hours=1', etc.)
    scheduler.add_job(pipeline_job, 'interval', minutes=5)
    
    print("Iniciando el servicio de automatización. Presiona Ctrl+C para salir.")
    
    try:
        # Ejecutar un job inmediatamente al iniciar
        print("Ejecutando un job inicial...")
        pipeline_job()
        # Iniciar el bucle del scheduler
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Servicio detenido.")

if __name__ == "__main__":
    main()
