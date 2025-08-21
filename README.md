# 🤖 AI Content Creator

Este proyecto es un agente de IA autónomo que automatiza la creación de videos cortos (estilo Reels/Shorts) a partir de una simple idea. El sistema gestiona el ciclo completo: desde la generación del guion y la creación de todos los recursos multimedia (imágenes, videoclips y sonido) hasta la publicación en redes sociales.

## ✨ Características Principales

- **Orquestación con Agentes de IA**: Todo el flujo de trabajo está gestionado por un grafo de estados (`StateGraph`) implementado con **LangGraph**. Esto permite una arquitectura robusta, modular y con un manejo de errores centralizado.
- **Generación de Guiones Avanzada**: Un LLM (GPT-4o) crea una estructura de guion completa, incluyendo una narrativa por escenas, prompts optimizados para IA visual y hashtags relevantes.
- **Pipeline Multimedia Completo**: 
    - **Imágenes**: Genera imágenes fotorrealistas con **Ideogram v3 Turbo**.
    - **Video**: Anima las imágenes estáticas para crear clips dinámicos con **Seedance-1-Pro**.
    - **Audio**: Crea una pista de sonido ambiental para el video final con **MMAudio**.
- **Publicación Automatizada**: Integra la **API Graph de Instagram** para publicar los videos generados directamente como Reels.
- **Arquitectura Escalable con Docker**: Todo el entorno, incluida la aplicación y la base de datos **PostgreSQL**, está contenedorizado con Docker, garantizando consistencia y facilidad de despliegue.
- **Persistencia y Estado**: Utiliza una base de datos PostgreSQL para registrar el estado de cada proyecto, permitiendo la trazabilidad y la recuperación ante fallos.

## 🛠️ Stack Tecnológico

- **Orquestación de Agentes**: LangChain, LangGraph
- **Modelos de Lenguaje (LLM)**: OpenAI (GPT-4o)
- **Generación Multimedia (vía API)**: Replicate
  - **Texto a Imagen**: `ideogram-ai/ideogram-v3-turbo`
  - **Imagen a Video**: `bytedance/seedance-1-pro`
  - **Texto a Audio**: `zsxkib/mmaudio`
- **Base de Datos**: PostgreSQL (orquestado con Docker)
- **Infraestructura**: Docker, Docker Compose
- **Publicación**: API Graph de Instagram

## 📂 Estructura del Proyecto

```
ai-content-creator/
├── src/
│   ├── agents/             # Define el grafo de LangGraph y los nodos del flujo.
│   ├── assets/             # Recursos generados (imágenes, videos, audio).
│   ├── database/           # Modelos SQLAlchemy y gestión de la sesión de BD.
│   ├── logic/              # Lógica de negocio: generadores, editores, publicadores.
│   └── config.py           # Carga y valida la configuración y variables de entorno.
├── .env.example            # Plantilla para las variables de entorno.
├── docker-compose.yml      # Orquesta los servicios de la aplicación y la base de datos.
├── Dockerfile              # Define el contenedor de la aplicación Python.
├── main.py                 # Punto de entrada de la aplicación.
└── requirements.txt        # Dependencias de Python.
```

## 🚀 Cómo Empezar

### Prerrequisitos

- Docker y Docker Compose instalados.
- Una cuenta de OpenAI y una API key.
- Una cuenta de Replicate y un API token.
- Credenciales para la API Graph de Instagram (`ACCOUNT_ID`, `ACCESS_TOKEN`) y una URL pública (ej. con `ngrok`) para que la API de Instagram pueda acceder al video.

### Instalación y Ejecución

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd ai-content-creator
    ```

2.  **Configura las variables de entorno:**
    Copia el archivo `.env.example` a `.env` y rellena **todas** las variables:
    ```bash
    cp .env.example .env
    ```
    Edita el archivo `.env` con tus claves y configuraciones. Asegúrate de que las variables de PostgreSQL coinciden con las usadas en `docker-compose.yml`.

3.  **Levanta los servicios con Docker Compose:**
    Este comando construirá la imagen de la aplicación, iniciará un contenedor para la base de datos PostgreSQL y ejecutará la aplicación.
    ```bash
    docker-compose up --build
    ```

4.  **Ejecuta el pipeline:**
    La aplicación se iniciará automáticamente. Sigue las instrucciones en la terminal para introducir una idea y comenzar el proceso de generación de contenido.

## 🔮 Futuro del Proyecto

- **Interfaz de Usuario**: Desarrollar una interfaz web (ej. con FastAPI y React/Vue) para gestionar y visualizar los proyectos de video de forma interactiva.
- **Agente de Planificación de Contenido**: Crear un agente de nivel superior que, en lugar de recibir una idea, genere un calendario de contenido para una semana basándose en tendencias actuales.
- **Edición Avanzada de Video**: Implementar un nodo en el grafo que ensamble los clips individuales en un único video final, añadiendo transiciones y sincronizando el audio de forma más precisa.
