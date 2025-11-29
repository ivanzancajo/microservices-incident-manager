# Usamos una imagen ligera de Python (igual que en tus otros servicios backend)
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos curl (útil para healthchecks) y limpiamos caché para reducir peso
RUN apt-get update && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

# Copiamos primero los requirements para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiamos el código (tu main.py) al contenedor
COPY . .

# Comando de arranque: ejecuta uvicorn buscando la app en 'main.py'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]