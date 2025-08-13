from pydantic import BaseModel, Field
from typing import List

class Scene(BaseModel):
    """Define la estructura de una única escena, incluyendo prompts para imagen y video."""
    scene_description: str = Field(
        description="Descripción narrativa y concisa de la escena (5-15 palabras)."
    )
    image_prompt: str = Field(
        description="Prompt detallado y optimizado para generar la imagen estática de la escena, como una lista de palabras clave."
    )
    video_prompt: str = Field(
        description="Prompt de movimiento que describe la acción para animar la imagen (ej: 'Slow zoom in on the character's face')."
    )

class ScriptStructure(BaseModel):
    """Define la estructura JSON esperada para el guion del video."""
    scenes: List[Scene] = Field(
        description="Lista de escenas, cada una con su descripción y prompts de imagen y video."
    )
    environment_prompt: str = Field(
        description="Un prompt que describe el ambiente general del video para dar consistencia a las imágenes."
    )
    audio_prompt: str = Field(
        description="Un prompt para generar el audio o sonido ambiente del video."
    )
    hashtags: List[str] = Field(description="Lista de hashtags virales para redes sociales.")
