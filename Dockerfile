# Use uma imagem base oficial do Python.
# A versão 'slim' é menor e ideal para produção.
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container.
WORKDIR /app

# Copie o arquivo de dependências primeiro.
# Isso aproveita o cache do Docker: se o arquivo não mudar,
# o passo de instalação não será executado novamente.
COPY requirements.txt .

# Instale as dependências listadas no requirements.txt.
# --no-cache-dir cria uma imagem menor.
RUN pip install --no-cache-dir -r requirements.txt

# Copie o resto dos arquivos da sua aplicação para o diretório de trabalho.
COPY . .

# Exponha a porta em que o Flask estará rodando.
EXPOSE 5000

# O comando para iniciar a sua aplicação quando o container for executado.
CMD ["python", "app.py"]
