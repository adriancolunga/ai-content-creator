import os
import replicate
import requests
from src.config import REPLICATE_API_TOKEN


if REPLICATE_API_TOKEN:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

def _download_video(url: str, save_path: str):
    """Descarga un archivo de video desde una URL y lo guarda localmente."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() 
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video descargado y guardado en: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el video desde {url}: {e}")
        raise

def generate_videos_from_images(idea_id: int, image_paths: list[str], video_prompts: list[str], audio_prompt: str = None) -> list[str]:
    """
    Genera un video corto para cada imagen proporcionada utilizando la API de Replicate.

    Args:
        idea_id (int): El ID de la idea, usado para nombrar los archivos de salida.
        image_paths (list[str]): Una lista de rutas a los archivos de imagen locales.
        video_prompts (list[str]): Una lista de prompts de texto para guiar la animación del video.

    Returns:
        list[str]: Una lista de rutas a los archivos de video generados.
    """
    print(f"Iniciando la generación de videos para la idea ID: {idea_id}")
    video_paths = []
    video_dir = os.path.join("src", "assets", "videos")
    os.makedirs(video_dir, exist_ok=True)

    if len(image_paths) != len(video_prompts):
        raise ValueError("La cantidad de imágenes y prompts de video no coincide.")

    for i, image_path in enumerate(image_paths):
        video_prompt = video_prompts[i]
        print(f"Procesando imagen {i+1}/{len(image_paths)}: {image_path}")
        print(f"  \_ Con prompt de video: '{video_prompt}'")
        try:
            with open(image_path, "rb") as image_file:
                output_url = replicate.run(
                    "bytedance/seedance-1-pro",
                    input={
                        "first_frame_image": image_file,
                        "prompt": video_prompt,
                        "resolution": "720p"
                    }
                )
            
            if not output_url:
                raise ValueError("La API de Replicate no devolvió una URL de salida.")

            if isinstance(output_url, list):
                output_url = output_url[0]

            print(f"URL del video generado por Replicate: {output_url}")

            video_filename = f"{idea_id}_{i}_final.mp4"
            save_path = os.path.join(video_dir, video_filename)
            _download_video(output_url.url, save_path)

            if audio_prompt:
                print(f" \_ Generando audio para el video: '{audio_prompt}'")
                with open(save_path, "rb") as video_file:
                    audio_video_output = replicate.run(
                        "zsxkib/mmaudio:62871fb59889b2d7c13777f08deb3b36bdff88f7e1d53a50ad7694548a41b484",
                        input={
                            "video": video_file,
                            "prompt": audio_prompt
                        }
                    )
                
                final_video_path = save_path.replace('.mp4', '_with_audio.mp4')
                _download_video(audio_video_output.url, final_video_path)
                video_paths.append(final_video_path)
            else:
                video_paths.append(save_path)

            # # ----------------
            # save_path = "src/assets/videos/87_ae7a7fa1_0_final_with_audio.mp4"
            # video_paths.append(save_path)
            # # ----------------

        except replicate.exceptions.ReplicateError as e:
            print(f"Error de la API de Replicate al procesar {image_path}: {e}")
            raise
        except Exception as e:
            print(f"Un error inesperado ocurrió al procesar {image_path}: {e}")
            raise

    print(f"Generación de videos completada. {len(video_paths)} videos creados.")
    return video_paths
