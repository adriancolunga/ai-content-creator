# AI Content Creator

This project is an autonomous AI agent that automates the creation of short videos (Reels/Shorts style) from a simple idea. The system manages the entire cycle: from script generation and the creation of all multimedia assets (images, video clips, and sound) to social media publishing.

## Key Features

- **AI Agent Orchestration**: The entire workflow is managed by a state graph (`StateGraph`) implemented with **LangGraph**. This allows for a robust, modular architecture with centralized error handling.
- **Advanced Script Generation**: An LLM (GPT-4o) creates a complete script structure, including a scene-based narrative, visual AI-optimized prompts, and relevant hashtags.
- **Complete Multimedia Pipeline**:
- **Images**: Generates photorealistic images.
- **Video**: Animate static images to create dynamic clips.
- **Audio**: Create an ambient soundtrack for the final video.
- **Scalable Architecture with Docker**: The entire environment, including the application and the **PostgreSQL** database, is containerized with Docker, ensuring consistency and ease of deployment.
- **Persistence and State**: Uses a PostgreSQL database to record the state of each project, enabling traceability and disaster recovery.

## Technology Stack

- **Agent Orchestration**: LangChain, LangGraph
- **Language Models (LLM)**: OpenAI (GPT-4o)
- **Multimedia Generation (via API)**: Replicate
- **Text to Image**
- **Image to Video**
- **Text to Audio**
- **Database**: PostgreSQL
- **Infrastructure**: Docker, Docker Compose
- **Publishing**: Instagram Graph API

## Project Structure

```
ai-content-creator/
├── src/
│ ├── agents/ # Defines the LangGraph graph and flow nodes.
│ ├── assets/ # Generated resources (images, videos, audio).
│ ├── database/ # SQLAlchemy models and database session management.
│ ├── logic/ # Business logic: generators, editors, publishers.
│ └── config.py # Loads and validates configuration and environment variables.
├── .env.example # Template for environment variables.
├── docker-compose.yml # Orchestrates application and database services.
├── Dockerfile # Defines the Python application container.
├── main.py # Application entry point.
└── requirements.txt # Python dependencies.
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.
- An OpenAI account and an API key.
- A Replicate account and an API token.

### Installation and Running

1. **Clone the repository:**
```bash
git clone <REPOSITORY_URL>
cd ai-content-creator
```

2. **Set the environment variables:**
Copy the `.env.example` file to `.env` and fill in **all** the variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your keys and settings. Make sure the PostgreSQL variables match those used in `docker-compose.yml`.

3. **Start the services with Docker Compose:**
This command will build the application image, start a container for the PostgreSQL database, and run the application.
```bash
docker-compose up --build
```

4. **Run the pipeline:**
The application will start automatically. Follow the instructions in the terminal to enter an idea and begin the content generation process.

## Future of the Project

- **User Interface**: Develop a web interface (e.g., with FastAPI and React/Vue) to manage and visualize video projects interactively.
- **Content Planning Agent**: Create a higher-level agent that, instead of receiving an idea, generates a content calendar for a week based on current trends.
- **Advanced Video Editing**: Implement a node in the graph that assembles individual clips into a single final video, adding transitions and synchronizing audio more precisely.