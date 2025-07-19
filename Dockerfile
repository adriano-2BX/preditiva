# Use a imagem base padrão do Python, que é mais completa e evita erros.
FROM python:3.9

# Defina o diretório de trabalho dentro do container.
WORKDIR /app

# Copie o arquivo de dependências.
COPY requirements.txt .

# Instale as dependências Python.
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do projeto para o container.
# Isto inclui o app.py e a pasta 'templates' com o index.html.
COPY . .

# Exponha a porta em que o Flask estará rodando.
EXPOSE 5000

# O comando para iniciar a aplicação.
CMD ["python", "app.py"]
