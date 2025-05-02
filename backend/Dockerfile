FROM python:3.9-slim

WORKDIR /app

# 1. Instalar dependências do sistema (camada raramente alterada)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-por \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Copiar apenas o requirements.txt primeiro (camada intermediária)
COPY requirements.txt .

# 3. Instalar dependências Python (cacheada separadamente)
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o resto dos arquivos (camada que muda frequentemente)
COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]