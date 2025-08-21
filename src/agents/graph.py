import uuid
from langgraph.graph import StateGraph, END
from sqlalchemy.orm import Session
from .state import AppState
from ..database.database import get_db
from ..database.models import VideoProject
from ..logic import content_generator, multimedia_generator, social_publisher


def start_new_project(state: AppState) -> AppState:
    """Nodo inicial: Crea una nueva entrada en la base de datos para el proyecto."""
    try:
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
    except Exception as e:
        state['error'] = f"Error en start_new_project: {e}"
    return state

def generate_content_node(state: AppState) -> AppState:
    """Nodo para generar el guion y los prompts."""
    try:
        print("\n--- Nodo: Generando Contenido ---")
        with get_db() as db:
            project = db.query(VideoProject).filter(VideoProject.id == state['project_id']).one()
            project.status = 'generating_content'
            db.commit()

            # ----------
            # script_data = {"scenes": [{"scene_description": "Erudito salvando pergaminos entre llamas", "image_prompt": "ancient library engulfed in flames, scholar in traditional robes, scrolls in hands, dramatic lighting, intense fire, smoke, chaos, surreal, cinematic, photorealistic, 4K", "video_prompt": "Camera shakes slightly to simulate panic, flames flicker dynamically"}], "environment_prompt": "Ancient library with towering shelves, filled with scrolls and manuscripts, bathed in the warm glow of fire, chaotic and urgent atmosphere", "audio_prompt": "Crackling fire, distant shouting, rustle of scrolls, ominous background music", "hashtags": ["#HistoriaAntigua", "#BibliotecaDeAlejandr\u00eda", "#POVInmersivo"]}
            # ----------


            script_data = content_generator.generate_viral_script(state['idea'])

            if 'error' in script_data:
                raise ValueError(script_data['error'])
            
            state['script_data'] = script_data
            project.script = script_data
            db.commit()
    except Exception as e:
        state['error'] = f"Error en generate_content_node: {e}"
    return state

def generate_multimedia_node(state: AppState) -> AppState:
    """Nodo para generar imágenes y videos a partir del guion."""
    try:
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
            audio_path = multimedia_results.get('audio')

            if not image_paths or not video_paths:
                raise ValueError("Fallo en la generación de multimedia (imágenes o videos).")

            # Actualizar el estado para los siguientes nodos
            state['image_paths'] = image_paths
            state['video_paths'] = video_paths
            state['audio_path'] = audio_path

            project.assets_urls = {
                'images': image_paths, 
                'videos': video_paths,
                'audio': audio_path
            }
            # Guardamos la primera ruta de video como referencia principal, si existe
            project.video_path = video_paths[0] if video_paths else None
            project.status = 'multimedia_completed'
            db.commit()
    except Exception as e:
        state['error'] = f"Error en generate_multimedia_node: {e}"
    return state

def publish_video_node(state: AppState) -> AppState:
    """Nodo para publicar el video en las plataformas sociales. TEMPORALMENTE EN PAUSA."""
    try:
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
    except Exception as e:
        state['error'] = f"Error en publish_video_node: {e}"
    return state

def handle_error_node(state: AppState) -> AppState:
    """Nodo para manejar errores, actualizar la BD y finalizar."""
    error_message = state.get('error', 'Error desconocido')
    print(f"\n--- ERROR DETECTADO ---")
    print(f"Error: {error_message}")
    
    project_id = state.get('project_id')
    if project_id:
        with get_db() as db:
            try:
                project = db.query(VideoProject).filter(VideoProject.id == project_id).one()
                project.status = 'failed'
                db.commit()
                print(f"El estado del proyecto {project_id} ha sido actualizado a 'failed'.")
            except Exception as db_error:
                print(f"Error adicional al intentar actualizar la base de datos: {db_error}")
    
    return state

def decide_next_node(state: AppState):
    """Determina el siguiente nodo a ejecutar basándose en si ocurrió un error."""
    if state.get('error'):
        return "handle_error"
    # Si no hay un campo 'error', o si está vacío/None, continuamos
    return "continue"
    

workflow = StateGraph(AppState)

workflow.add_node("start_project", start_new_project)
workflow.add_node("generate_content", generate_content_node)
workflow.add_node("generate_multimedia", generate_multimedia_node)
workflow.add_node("publish_video", publish_video_node)
workflow.add_node("handle_error", handle_error_node)

workflow.set_entry_point("start_project")

workflow.add_conditional_edges(
    "start_project",
    decide_next_node,
    {"continue": "generate_content", "handle_error": "handle_error"}
)
workflow.add_conditional_edges(
    "generate_content",
    decide_next_node,
    {"continue": "generate_multimedia", "handle_error": "handle_error"}
)
workflow.add_conditional_edges(
    "generate_multimedia",
    decide_next_node,
    {"continue": "publish_video", "handle_error": "handle_error"}
)

workflow.add_edge("publish_video", END)
workflow.add_edge("handle_error", END)

app = workflow.compile()

def get_graph():
    """Retorna la aplicación del grafo compilado."""
    return app
