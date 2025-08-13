import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# --- Project Settings ---
NUM_SCENES = int(os.getenv("NUM_SCENES", 3))

# --- API Keys & Credentials ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Credenciales de Instagram Graph API
INSTAGRAM_ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')

# ngrok
NGROK_PUBLIC_URL = os.getenv('NGROK_PUBLIC_URL')

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./content_creator.db")

# --- Validation ---
def check_env_vars():
    """Verifica que las variables de entorno esenciales estén configuradas."""
    required_vars = {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "HF_TOKEN": HF_TOKEN,
        "REPLICATE_API_TOKEN": REPLICATE_API_TOKEN,
        "DATABASE_URL": DATABASE_URL
    }
    
    missing_vars = [name for name, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(f"Las siguientes variables de entorno requeridas no están configuradas: {', '.join(missing_vars)}")



    # Advertir sobre credenciales opcionales de Instagram Graph API
    if not INSTAGRAM_ACCOUNT_ID or not INSTAGRAM_ACCESS_TOKEN:
        print("Advertencia: Las credenciales de Instagram Graph API (INSTAGRAM_ACCOUNT_ID, INSTAGRAM_ACCESS_TOKEN) no están configuradas. La publicación en Instagram fallará.")

    print("Configuración cargada correctamente.")

if __name__ == '__main__':
    try:
        check_env_vars()
        print(f"URL de la base de datos: {DATABASE_URL}")
    except ValueError as e:
        print(f"Error de configuración: {e}")
