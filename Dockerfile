# Use a imagem base padrão do Python.
FROM python:3.9

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Instala dependências do sistema que podem ser necessárias para alguns pacotes
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências.
COPY requirements.txt .

# Instala as dependências Python.
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o container.
COPY . .

# Expõe a porta em que o Flask estará rodando.
EXPOSE 5000

# O comando para iniciar a aplicação web.
# O worker.py deve ser executado como um serviço separado no Easypanel.
CMD ["python", "app.py"]

