FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema de forma limpia
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    libgl1 \
    libglib2.0-0 \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# 1. Instalar PyTorch y Torchvision versión CPU desde su índice oficial
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 2. Instalar el resto de las librerías del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]