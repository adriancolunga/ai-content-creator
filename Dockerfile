# Usa una imagen base de Python oficial y ligera
FROM python:3.11-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala las dependencias del sistema si fueran necesarias (ej. para librerías de video)
# RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

# Copia el archivo de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al directorio de trabajo
COPY ./src ./src
COPY main.py .

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
