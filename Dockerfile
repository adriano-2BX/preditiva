# Use a imagem base padrão do Python.
FROM python:3.9

# Defina o diretório de trabalho dentro do container.
WORKDIR /app

# --- PASSO DE CORREÇÃO: ATUALIZAR O PIP ---
# Garante que estamos a usar a versão mais recente do instalador de pacotes,
# o que resolve muitos problemas de instalação de dependências.
RUN pip install --upgrade pip

# Copie o arquivo de dependências primeiro para otimizar o cache.
COPY requirements.txt .

# Instale as dependências Python.
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
