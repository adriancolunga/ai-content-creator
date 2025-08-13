# 🤖 Viral Content Creator AI

Este proyecto es un pipeline automatizado de generación de contenido de video, diseñado para transformar una simple idea en una serie de videos cortos (estilo Reels/Shorts) inmersivos y listos para publicar en redes sociales. Utiliza una arquitectura modular basada en agentes de IA para orquestar el proceso completo, desde la creación del guion hasta la generación de los recursos multimedia.

## ✨ Características Principales

- **Generación de Guiones con IA:** A partir de una idea inicial, un LLM (GPT-4o) genera una estructura de guion completa, incluyendo una narrativa secuencial de escenas, una descripción del entorno y hashtags relevantes.
- **Prompts Optimizados:** El sistema transforma las descripciones de las escenas en prompts altamente optimizados (basados en palabras clave) para modelos de texto-a-imagen, mejorando drásticamente la calidad y coherencia de las imágenes.
- **Generación de Imágenes POV:** Utiliza modelos de difusión (como Stable Diffusion a través de la API de Hugging Face) para crear imágenes fotorrealistas y cinematográficas desde una perspectiva en primera persona (POV).
- **Orquestación Modular con LangGraph:** Todo el flujo de trabajo está gestionado por un grafo de estados (Stateful Graph) implementado con LangGraph, lo que permite una gran flexibilidad, modularidad y un manejo de errores robusto.
- **Arquitectura Escalable:** El código está organizado en módulos lógicos (generación de contenido, multimedia, edición de video, publicación), facilitando la adición de nuevas funcionalidades o el cambio de APIs (ej. cambiar de DALL-E a Stable Diffusion).

## 🛠️ Stack Tecnológico

- **Orquestación y Agentes IA:** LangChain, LangGraph
- **Modelos de Lenguaje (LLM):** OpenAI (GPT-4o)
- **Generación de Imágenes:** Hugging Face Inference API (Stable Diffusion)
- **Edición de Video (futuro):** MoviePy
- **Gestión de Dependencias:** Pip (ver `requirements.txt`)
- **Base de Datos (futuro):** SQLAlchemy con SQLite

## 📂 Estructura del Proyecto

```
content-creator-2/
├── src/
│   ├── agents/             # Define el grafo de LangGraph y los nodos del flujo
│   │   └── graph.py
│   ├── logic/              # Contiene la lógica de negocio principal
│   │   ├── content_generator.py  # Generación de guiones y prompts
│   │   ├── multimedia_generator.py # Generación de imágenes y audio
│   │   ├── video_editor.py       # Edición y composición de video
│   │   └── ...
│   └── data/               # Modelos de base de datos (SQLAlchemy)
├── assets/                 # Directorio para los recursos generados (imágenes, videos)
├── .env                    # Archivo para variables de entorno (API keys)
├── main.py                 # Punto de entrada de la aplicación
└── requirements.txt        # Dependencias de Python
```

## 🚀 Cómo Empezar

### Prerrequisitos

- Python 3.9+
- Una cuenta de OpenAI y una API key.
- Una cuenta de Hugging Face y un API token.

### Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd content-creator-2
    ```

2.  **Crea y activa un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto y añade tus claves de API:
    ```env
    OPENAI_API_KEY="tu_api_key_de_openai"
    HF_TOKEN="tu_api_token_de_hugging_face"
    NUM_SCENES=5
    ```

### Ejecución

Para iniciar el pipeline, ejecuta el script principal:

```bash
python main.py
```

El programa te pedirá que introduzcas una idea para el video, y comenzará el proceso de generación de contenido. Los resultados se guardarán en la carpeta `assets/`.

## 🔮 Futuro del Proyecto

- **Generación de Video por IA:** Integrar un modelo de Image-to-Video (ej. Stable Video Diffusion) para convertir las imágenes estáticas en clips de video dinámicos.
- **Sonido Ambiental:** Implementar la generación de audio a partir de prompts usando APIs como la de ElevenLabs o Stability AI.
- **Publicación Automática:** Desarrollar los módulos de `social_publisher` para subir el contenido final directamente a plataformas como YouTube, TikTok e Instagram.
