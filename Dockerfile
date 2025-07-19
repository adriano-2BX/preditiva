# Use uma imagem base oficial do Python.
# A versão 'slim' é mais pequena e ideal para produção.
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contentor.
WORKDIR /app

# Copie o ficheiro de dependências primeiro para otimizar a cache.
COPY requirements.txt .

# Instale as dependências.
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os ficheiros da sua aplicação (app.py, train_model.py).
COPY . .

# --- PASSO CRÍTICO: TREINE O MODELO DURANTE A CONSTRUÇÃO ---
# Este comando executa o script de treino, gerando o ficheiro do modelo.
RUN python train_model.py

# Exponha a porta em que o Flask estará a ser executado.
EXPOSE 5000

# O comando para iniciar a API (que agora usa o modelo já treinado).
CMD ["python", "app.py"]
