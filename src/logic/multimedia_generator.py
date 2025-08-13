import os
from pathlib import Path
from typing import List, Dict, Optional
import requests
from openai import OpenAI
from ..config import OPENAI_API_KEY
import replicate
from .video_editor import generate_videos_from_images

# --- Configuración de Directorios ---
ASSETS_DIR = Path(__file__).parent.parent / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
AUDIO_DIR = ASSETS_DIR / "audio"

# Crear directorios si no existen
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)



# --- Generación de Audio ---

def generate_ambient_sound(audio_prompt: str, project_id: str) -> Optional[str]:
    """
    Placeholder para la futura implementación de generación de sonido ambiental.

    En el futuro, esta función usará una API como la de Stability AI (Stable Audio)
    para generar un paisaje sonoro basado en el prompt.

    Args:
        audio_prompt: El prompt de texto para generar el audio.
        project_id: Un identificador único del proyecto para nombrar el archivo.

    Returns:
        La ruta al archivo de audio generado o None si no se implementa.
    """
    print("\nADVERTENCIA: La generación de sonido ambiental no está implementada.")
    print(f"Prompt de audio recibido: '{audio_prompt}'")
    # Cuando se implemente, aquí iría la llamada a la API de audio.
    # Por ahora, simplemente no se genera ningún archivo.
    return None

# --- Generación de Imágenes ---

def _download_image(url: str, save_path: Path):
    """Descarga una imagen desde una URL y la guarda localmente."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Imagen descargada y guardada en: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen desde {url}: {e}")
        raise

def generate_scene_images(scenes: List[Dict[str, str]], project_id: str) -> List[str]:
    """
    Genera una imagen para cada escena utilizando Replicate (ideogram-v3-turbo).

    Args:
        scenes: Una lista de diccionarios, donde cada uno contiene el 'image_prompt'.
        project_id: Un identificador único para nombrar los archivos.

    Returns:
        Una lista de rutas a las imágenes generadas.
    """
    image_paths = []
    if not scenes:
        print("Advertencia: No hay escenas para generar imágenes.")
        return image_paths

    for i, scene in enumerate(scenes):
        prompt = scene.get('image_prompt')
        if not prompt:
            print(f"Advertencia: La escena {i+1} no tiene un prompt de imagen.")
            continue

        file_name = f"{project_id}_scene_{i+1}.png"
        image_path = IMAGES_DIR / file_name

        print(f"Generando imagen para la escena {i+1}/{len(scenes)}")
        print(f"  \_ Con prompt de imagen: '{prompt}'")
        try:
            input_data = {
                "prompt": prompt,
                "aspect_ratio": "9:16"
            }

            # La API de ideogram-ai/ideogram-v3-turbo devuelve una LISTA de objetos FileOutput
            output_list = replicate.run(
                "ideogram-ai/ideogram-v3-turbo",
                input=input_data
            )

            # La documentación muestra que puedes obtener la URL de cada FileOutput.
            # Como la mayoría de los modelos devuelven una lista, tomamos el primer elemento.
            if output_list and isinstance(output_list, list):
                file_output_object = output_list[0]
                # Accedemos a la propiedad .url (sin paréntesis)
                image_url = file_output_object.url
            else:
                # En caso de que no devuelva una lista (por ejemplo, si devuelve un solo objeto)
                # Se asume que el output es el objeto FileOutput directamente.
                image_url = output_list.url

            # image_url = "src/assets/images/79_a265a246_scene_1.png"

            # Validaciones sobre la URL
            if not image_url or not isinstance(image_url, str):
                raise ValueError("La salida de la API no es una URL válida.")

            if not image_url.startswith('https'):
                raise ValueError(f"La URL procesada no es válida: '{image_url}'")
    
            _download_image(image_url, image_path)    
            image_paths.append(str(image_path))

        except Exception as e:
            print(f"Error al generar la imagen para la escena {i+1}: {e}")
            continue

    return image_paths

def generate_multimedia_for_idea(script_data: Dict, project_id: str) -> Dict[str, List[str]]:
    """
    Orquesta la generación de todo el contenido multimedia para una idea.

    Primero genera las imágenes para cada escena, y luego genera un video
    corto para cada una de esas imágenes usando su prompt de video correspondiente.

    Args:
        script_data: El diccionario completo del guion, incluyendo la lista de escenas.
        project_id: El ID único del proyecto.

    Returns:
        Un diccionario con las rutas a los archivos generados ('images' y 'videos').
    """
    multimedia_paths = {
        "images": [],
        "videos": []
    }
    scenes = script_data.get('scenes', [])
    if not scenes:
        print("El guion no contiene escenas. No se puede generar multimedia.")
        return multimedia_paths

    # 1. Generar imágenes
    image_paths = generate_scene_images(scenes, project_id)
    if not image_paths:
        print("No se generaron imágenes. Deteniendo el proceso de generación de video.")
        return multimedia_paths
    
    multimedia_paths["images"] = image_paths

    # 2. Extraer prompts de video y generar los videos
    video_prompts = [scene.get('video_prompt', '') for scene in scenes]
    video_paths = generate_videos_from_images(project_id, image_paths, video_prompts)
    multimedia_paths["videos"] = video_paths

    return multimedia_paths


# --- Ejemplo de Uso (para pruebas) ---
if __name__ == '__main__':
    # Simular datos de un guion generado
    test_project_id = "cleopatra_test_01"
    test_audio_prompt = "Viento del desierto, arena, atmósfera misteriosa y antigua, con un toque de majestuosidad."
    test_scenes_data = [
        {
            'scene_description': 'Cleopatra en un carro dorado',
            'image_prompt': 'Photorealistic, 4K, cinematic shot of Cleopatra on a majestic golden chariot entering ancient Rome. The streets are filled with cheering crowds. Majestic Roman architecture is visible. Golden hour light. Cleopatra looks proud and defiant. Epic composition.'
        },
        {
            'scene_description': 'Cleopatra observando el Senado Romano',
            'image_prompt': 'Ultra-realistic, 4K, cinematic still of Cleopatra standing on a balcony, looking down at the Roman Senate. She is draped in royal blue and gold. Her expression is a mix of curiosity and strategic calculation. The lighting is dramatic, with long shadows. Focus on her intense gaze.'
        }
    ]

    print("--- INICIANDO PRUEBA DE GENERACIÓN DE MULTIMEDIA ---")
    
    # 1. Probar generación de audio
    # 1. Probar generación de audio (actualmente es un placeholder)
    audio_file = generate_ambient_sound(test_audio_prompt, test_project_id)
    if audio_file:
        print(f"\nPrueba de audio exitosa. Archivo: {audio_file}")
    else:
        print("\nPrueba de audio fallida.")

    # 2. Probar el flujo completo de generación de multimedia (imágenes y videos)
    # Primero, necesitamos un guion completo que incluya los video_prompts
    from .content_generator import generate_viral_script
    print("\n--- Generando Guion Completo para la Prueba ---")
    test_idea = "Cleopatra entrando a Roma por primera vez, no como prisionera, sino como conquistadora silenciosa."
    full_script_data = generate_viral_script(test_idea)

    if 'error' in full_script_data:
        print(f"Error al generar el guion de prueba: {full_script_data['error']}")
        exit()

    print("--- Guion de Prueba Generado ---")
    # print(json.dumps(full_script_data, indent=2, ensure_ascii=False))

    multimedia_results = generate_multimedia_for_idea(full_script_data, test_project_id)
    print("\n--- Resultados de la Generación de Multimedia ---")
    if multimedia_results["images"]:
        print(f"{len(multimedia_results['images'])} imágenes generadas:")
        for f in multimedia_results['images']:
            print(f"- {f}")
    else:
        print("Fallo en la generación de imágenes.")

    if multimedia_results["videos"]:
        print(f"\n{len(multimedia_results['videos'])} videos generados:")
        for f in multimedia_results['videos']:
            print(f"- {f}")
    else:
        print("\nFallo en la generación de videos.")
