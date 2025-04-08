# Usa uma imagem base do Python
FROM python:3.10-slim

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto
COPY . /app/

# Instala as dependências Python
RUN pip install --no-cache-dir -e .

# Define o comando padrão
ENTRYPOINT ["file-analyzer"] 