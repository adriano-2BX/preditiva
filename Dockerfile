# Use a imagem base padrão do Python, que já inclui as ferramentas de compilação.
# Esta é a correção para o erro 'apt-get exit code 100'.
FROM python:3.9

# Defina o diretório de trabalho dentro do container.
WORKDIR /app

# Copie o arquivo de dependências primeiro para otimizar o cache.
COPY requirements.txt .

# Instale as dependências Python.
# Não precisamos mais do passo 'apt-get' com esta imagem base.
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
