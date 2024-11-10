# Imagem base
FROM python:3.11-slim

# Instalação de dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Criação de diretório de trabalho
WORKDIR /website

# Copiar o código da aplicação para o container
COPY . .

# Expor a porta 8000
EXPOSE 8000

# Comando de inicialização da aplicação
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]