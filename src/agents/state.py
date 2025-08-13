from typing import TypedDict, List, Dict, Optional, Any

class AppState(TypedDict):
    """
    Define la estructura del estado que se pasará entre los nodos del grafo.
    Este estado contiene toda la información necesaria para un flujo de trabajo de video.
    """
    # --- Identificadores y Entradas ---
    project_id: int          # ID del proyecto en la base de datos
    idea: str                # La idea inicial para el video

    # --- Contenido Generado ---
    script_data: Dict[str, Any]  # El guion completo con escenas, prompts, etc.
    
    # --- Rutas de Archivos Locales ---
    image_paths: List[str]   # Lista de rutas a las imágenes generadas
    audio_path: str          # Ruta al archivo de audio de la narración
    video_path: str          # Ruta al archivo de video final

    # --- Resultados y Errores ---
    published_urls: Dict[str, str] # URLs de publicación en redes sociales
    error: Optional[str]         # Mensaje de error si algo falla
    retries: int                 # Contador de reintentos para manejar fallos
