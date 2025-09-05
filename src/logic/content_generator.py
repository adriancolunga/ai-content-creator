import json
from typing import Dict, Any, List
from ..config import OPENAI_API_KEY, NUM_SCENES
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from .schemas import ScriptStructure


# 1. Plantilla para generar la estructura completa del video, incluyendo prompts de imagen y video.
script_structure_template = """
Eres una IA avanzada especializada en la creación de guiones para videos cortos virales de estilo POV (primera persona).
Tu tarea es generar una estructura completa para un video basado en el tema proporcionado, incluyendo prompts detallados para la generación de imágenes y videos.

**Idea:** "{idea}"

**Instrucciones Generales:**
1.  **Número de Escenas:** Crea exactamente {num_scenes} escenas.
2.  **Narrativa Coherente:** Las escenas deben contar una historia secuencial y lógica.
3.  **Perspectiva POV:** Todas las escenas deben estar en primera persona (POV) para maximizar la inmersión.

**Instrucciones por cada Escena:**
Para cada una de las {num_scenes} escenas, debes generar:
1.  **`scene_description`**: Un título o descripción concisa y potente de la escena (5-15 palabras).
2.  **`image_prompt`**: Un prompt optimizado para un modelo de texto-a-imagen (ej. Stable Diffusion). Debe ser una lista de palabras clave y frases cortas que describan una escena estática y visualmente impactante. Incluye estilo, composición y calidad (ej: `cinematic, photorealistic, 4K, epic composition`).
3.  **`video_prompt`**: Un prompt de movimiento que describa la acción para animar la imagen generada. Debe ser una frase corta y clara que indique el dinamismo (ej: `Slow zoom in on the character's face`, `Camera pans left to reveal a hidden city`, `Dust particles float in the air`).

**Además, genera:**
- **`environment_prompt`**: Una descripción del entorno general para dar consistencia visual.
- **`audio_prompt`**: Un prompt para generar un sonido ambiental que cubra todo el video.
- **`hashtags`**: Una lista de 3-5 hashtags relevantes.

**Formato de Salida Obligatorio:**
Devuelve únicamente un objeto JSON válido que se ajuste a la estructura Pydantic proporcionada. No añadas texto adicional.
"""

def generate_viral_script(idea: str) -> Dict[str, Any]:
    """Función principal que orquesta la generación del guion completo en una sola llamada a la IA."""
    print(f"Iniciando generación de guion para la idea: '{idea}'")

    llm = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=OPENAI_API_KEY)
    structured_llm = llm.with_structured_output(ScriptStructure)

    prompt = ChatPromptTemplate.from_template(script_structure_template)
    chain = prompt | structured_llm

    try:
        script_obj = chain.invoke({"idea": idea, "num_scenes": NUM_SCENES})
        final_script = script_obj.model_dump()

        print("Guion generado exitosamente.")
        return final_script

    except Exception as e:
        print(f"Error al generar la estructura del guion: {e}")
        return {"error": f"Error en la generación del guion: {e}"}

if __name__ == '__main__':
    test_idea = "Cleopatra entrando a Roma por primera vez, no como prisionera, sino como conquistadora silenciosa."
    
    final_script_data = generate_viral_script(test_idea)
    
    if 'error' not in final_script_data:
        print("\n--- GUION FINAL GENERADO ---")
        print(json.dumps(final_script_data, indent=2, ensure_ascii=False))
