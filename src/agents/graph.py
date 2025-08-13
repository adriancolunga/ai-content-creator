import uuid
from langgraph.graph import StateGraph, END
from sqlalchemy.orm import Session
from .state import AppState
from ..database.database import get_db
from ..database.models import VideoProject
from ..logic import content_generator, multimedia_generator, social_publisher

# --- Nodos del Grafo ---

def start_new_project(state: AppState) -> AppState:
    """Nodo inicial: Crea una nueva entrada en la base de datos para el proyecto."""
    with get_db() as db:
        new_project = VideoProject(
            idea_prompt=state['idea'],
            status='starting'
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        print(f"Nuevo proyecto iniciado con ID: {new_project.id}")
        state['project_id'] = new_project.id
    return state

def generate_content_node(state: AppState) -> AppState:
    """Nodo para generar el guion y los prompts."""
    print("\n--- Nodo: Generando Contenido ---")
    with get_db() as db:
        project = db.query(VideoProject).filter(VideoProject.id == state['project_id']).one()
        project.status = 'generating_content'
        db.commit()

        script_data = content_generator.generate_viral_script(state['idea'])
        if 'error' in script_data:
            raise ValueError(script_data['error'])
        
        state['script_data'] = script_data
        project.script = script_data
        db.commit()
    return state

def generate_multimedia_node(state: AppState) -> AppState:
    """Nodo para generar imágenes y videos a partir del guion."""
    print("\n--- Nodo: Generando Multimedia (Imágenes y Videos) ---")
    with get_db() as db:
        project = db.query(VideoProject).filter(VideoProject.id == state['project_id']).one()
        project.status = 'generating_multimedia'
        db.commit()

        script_data = state['script_data']
        project_id_str = f"{state['project_id']}_{uuid.uuid4().hex[:8]}"

        # Orquestar la generación de imágenes y videos
        multimedia_results = multimedia_generator.generate_multimedia_for_idea(script_data, project_id_str)

        image_paths = multimedia_results.get('images', [])
        video_paths = multimedia_results.get('videos', [])

        if not image_paths or not video_paths:
            raise ValueError("Fallo en la generación de multimedia (imágenes o videos).")

        # Actualizar el estado para los siguientes nodos
        state['image_paths'] = image_paths
        state['video_paths'] = video_paths
        # El audio_path se puede mantener si se genera en otro lado, aquí lo omitimos por ahora
        state['audio_path'] = None

        project.assets_urls = {'images': image_paths, 'videos': video_paths}
        # Guardamos la primera ruta de video como referencia principal, si existe
        project.video_path = video_paths[0] if video_paths else None
        project.status = 'multimedia_completed'
        db.commit()
    return state

def publish_video_node(state: AppState) -> AppState:
    """Nodo para publicar el video en las plataformas sociales. TEMPORALMENTE EN PAUSA."""
    print("\n--- Nodo: Publicación de Video (EN PAUSA) ---")
    video_paths = state.get('video_paths', [])
    
    if not video_paths:
        print("No hay videos generados para publicar. Finalizando el proceso.")
    else:
        print(f"{len(video_paths)} videos listos para ser publicados:")
        for path in video_paths:
            print(f"  - {path}")

    print("\nLa publicación automática está en pausa. Saltando este paso.")
    
    with get_db() as db:
        project = db.query(VideoProject).filter(VideoProject.id == state['project_id']).one()
        project.status = 'completed'
        project.published_urls = {'status': 'paused'}
        db.commit()
        print("\n¡PROCESO COMPLETADO CON ÉXITO!")
    return state

# --- Construcción del Grafo ---

workflow = StateGraph(AppState)

# Añadir nodos
workflow.add_node("start_project", start_new_project)
workflow.add_node("generate_content", generate_content_node)
workflow.add_node("generate_multimedia", generate_multimedia_node)
workflow.add_node("publish_video", publish_video_node)

# Definir el punto de entrada
workflow.set_entry_point("start_project")

# Añadir aristas (conexiones)
workflow.add_edge("start_project", "generate_content")
workflow.add_edge("generate_content", "generate_multimedia")
workflow.add_edge('generate_multimedia', 'publish_video')
workflow.add_edge("publish_video", END)

# Compilar el grafo
app = workflow.compile()

# Para añadir manejo de errores, se podría usar un `try-except` en cada nodo
# y dirigir al nodo `handle_error` en caso de excepción. 
# LangGraph también soporta aristas condicionales para esto, 
# pero un try-except explícito es más claro para empezar.

def get_graph():
    """Retorna la aplicación del grafo compilado."""
    return app
