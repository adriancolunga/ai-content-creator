import requests
import time
import os
import http.server
import socketserver
import threading
from typing import Dict, Any, Optional
from ..config import INSTAGRAM_ACCOUNT_ID, INSTAGRAM_ACCESS_TOKEN, NGROK_PUBLIC_URL

def publish_to_youtube(video_path: str, script_data: Dict[str, Any]) -> Optional[str]:
    """
    Placeholder para la función de publicación en YouTube.

    En una implementación real, esta función contendría:
    1.  El flujo de autenticación OAuth2 para obtener credenciales de usuario.
    2.  La construcción del cuerpo de la solicitud para la API de YouTube Data v3.
    3.  La subida del archivo de video.
    4.  El manejo de respuestas y errores de la API.

    Args:
        video_path: La ruta local al archivo de video final.
        script_data: El diccionario con los datos del guion (título, descripción, hashtags).

    Returns:
        La URL del video publicado o None si falla.
    """
    print("\n--- SIMULANDO PUBLICACIÓN EN YOUTUBE ---")
    print(f"Video a publicar: {video_path}")
    
    # Extraer título y descripción del guion
    # Se puede crear un título más dinámico si se desea
    title = script_data.get('idea', 'Video Generado por IA')
    description = script_data.get('narrator_script', '')
    hashtags = script_data.get('hashtags', [])
    full_description = f"{description}\n\n#{' #'.join(hashtags)}"

    print(f"Título: {title}")
    print(f"Descripción: {full_description[:100]}...")

    # Simular una subida exitosa
    print("¡Publicación simulada con éxito!")
    # Devolver una URL de YouTube de ejemplo
    simulated_url = f"https://www.youtube.com/shorts/simulated_{hash(video_path)}"
    return simulated_url

class VideoServerManager:
    """Context manager to serve a local file over a simple HTTP server."""
    def __init__(self, file_path: str):
        self.file_path = os.path.abspath(file_path)
        self.directory = os.path.dirname(self.file_path)
        self.filename = os.path.basename(self.file_path)
        self.port = 8000
        self.httpd = None
        self.thread = None
        self.original_directory = os.getcwd()

    def __enter__(self):
        if not NGROK_PUBLIC_URL:
            raise ValueError("La variable de entorno NGROK_PUBLIC_URL no está configurada.")

        os.chdir(self.directory)
        handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", self.port), handler)
        
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        print(f"Serving file '{self.filename}' from '{self.directory}' on port {self.port}")
        
        # Construir la URL pública usando la variable de entorno
        # Asegurarse de que la URL base no tenga una barra al final
        base_url = NGROK_PUBLIC_URL.rstrip('/')
        public_url = f"{base_url}/{self.filename}"
        print(f"Video accessible at: {public_url}")
        return public_url

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Shutting down local server...")
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        if self.thread:
            self.thread.join()
        os.chdir(self.original_directory)

def publish_to_instagram(video_path: str, script_data: Dict[str, Any]) -> Optional[str]:
    """
    Publica un video como un Reel en Instagram usando la API oficial de Instagram Graph.

    Args:
        video_path: La ruta local al archivo de video final.
        script_data: El diccionario con los datos del guion (idea, hashtags).

    Returns:
        La URL del Reel publicado o None si falla.
    """
    print("\n--- PUBLICANDO EN INSTAGRAM (API OFICIAL) ---")

    if not INSTAGRAM_ACCOUNT_ID or not INSTAGRAM_ACCESS_TOKEN:
        print("Error: Credenciales de Instagram Graph API no configuradas. Saltando publicación.")
        return None

    caption = script_data.get('idea', 'Un video increíble generado por IA.')
    hashtags = script_data.get('hashtags', [])
    if hashtags:
        caption += "\n\n" + " ".join([f"#{h.strip()}" for h in hashtags])

    API_VERSION = "v23.0"
    BASE_URL = f"https://graph.facebook.com/{API_VERSION}"
    try:
        with VideoServerManager(video_path) as video_url:
            print("Paso 1: Creando contenedor de medios...")
            create_container_url = f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media"
            create_params = {
                'media_type': 'REELS',
                'caption': caption,
                'share_to_feed': 'true',
                'access_token': INSTAGRAM_ACCESS_TOKEN
            }

            create_params['video_url'] = video_url
            print(f"Params: {create_params}")
            
            response = requests.post(create_container_url, params=create_params)
            response.raise_for_status()
            creation_id = response.json().get('id')
            if not creation_id:
                raise ValueError("No se pudo obtener el ID de creación del contenedor.")
            print(f"Contenedor creado con ID: {creation_id}")

            print("Paso 2: Esperando que el contenedor esté listo...")
            status_url = f"https://graph.facebook.com/{creation_id}"
            status_params = {'fields': 'status_code', 'access_token': INSTAGRAM_ACCESS_TOKEN}
        
            for _ in range(20):
                status_response = requests.get(status_url, params=status_params)
                status_response.raise_for_status()
                status = status_response.json().get('status_code')
                print(f"Estado actual del contenedor: {status}")
                if status == 'FINISHED':
                    break
                if status == 'ERROR':
                    raise Exception("Error en el procesamiento del contenedor de Instagram.")
                time.sleep(5)
            else:
                raise TimeoutError("El contenedor de Instagram no estuvo listo a tiempo.")

            print("Paso 3: Publicando el video...")
            publish_url = f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
            publish_params = {
                'creation_id': creation_id,
                'access_token': INSTAGRAM_ACCESS_TOKEN
            }
            publish_response = requests.post(publish_url, params=publish_params)
            publish_response.raise_for_status()
            media_id = publish_response.json().get('id')
            print(f"¡Publicación exitosa! Media ID: {media_id}")
        
            permalink_url = f"https://graph.facebook.com/{media_id}"
            permalink_params = {'fields': 'permalink', 'access_token': INSTAGRAM_ACCESS_TOKEN}
            permalink_response = requests.get(permalink_url, params=permalink_params)
            final_url = permalink_response.json().get('permalink')

            print(f"URL del Reel: {final_url}")
            return final_url

    except requests.exceptions.RequestException as e:
        print(f"!!! Error de red al comunicarse con la API de Instagram: {e} !!!")
        if e.response:
            print(f"Detalles del error: {e.response.text}")
        return None
    except Exception as e:
        print(f"!!! Error inesperado al publicar en Instagram: {e} !!!")
        return None
