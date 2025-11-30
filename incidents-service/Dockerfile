FROM python:3.11-slim

# Establecemos el directorio de trabajo
WORKDIR /code

# Instalamos dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos primero los requirements para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app /code/app

# Comando de arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]