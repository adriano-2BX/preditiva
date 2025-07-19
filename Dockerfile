# Use uma imagem base oficial do Python.
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container.
WORKDIR /app

# --- PASSO DE CORREÇÃO: INSTALAR DEPENDÊNCIAS DO SISTEMA ---
# A imagem 'slim' não vem com ferramentas de compilação.
# Alguns pacotes Python (como numpy, xgboost) precisam compilar código C/C++
# durante a instalação. Este comando instala essas ferramentas.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copie o arquivo de dependências primeiro para otimizar o cache.
COPY requirements.txt .

# Instale as dependências Python. Agora deve funcionar.
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos da sua aplicação (app.py, train_model.py).
COPY . .

# --- PASSO CRÍTICO: TREINE O MODELO DURANTE A CONSTRUÇÃO ---
# Este comando executa o script de treino, gerando o arquivo do modelo.
RUN python train_model.py

# Exponha a porta em que o Flask estará rodando.
EXPOSE 5000

# O comando para iniciar a API (que agora usa o modelo já treinado).
CMD ["python", "app.py"]
