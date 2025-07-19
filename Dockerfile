# Use a imagem base padrão do Python, que é mais completa e evita erros de rede.
FROM python:3.9

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Copia o arquivo de dependências.
COPY requirements.txt .

# Instala as dependências Python.
# A imagem base 'python:3.9' já contém as ferramentas necessárias para compilar.
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o container.
# Isto inclui o app.py, worker.py e a pasta 'templates'.
COPY . .

# Expõe a porta em que o Flask estará rodando.
EXPOSE 5000

# O comando para iniciar a aplicação web.
# O worker.py deve ser executado como um serviço separado no Easypanel.
CMD ["python", "app.py"]


