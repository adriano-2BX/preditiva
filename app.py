# ---- ESTÁGIO 1: O Construtor (Builder) ----
# Usamos uma imagem completa aqui para garantir que todas as ferramentas de build estejam presentes.
FROM python:3.11 AS builder

# Instala o Poetry
RUN pip install poetry

# Define o diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos de definição de dependência primeiro para otimizar o cache
COPY pyproject.toml poetry.lock* ./

# A MÁGICA ACONTECE AQUI:
# Exportamos as dependências para um arquivo requirements.txt padrão.
# Isso evita o `poetry install` no ambiente final.
# A flag --without-hashes é mais compatível com compilações em diferentes sistemas.
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Agora, instalamos as dependências usando o bom e velho pip a partir do arquivo gerado.
# Isso valida que as dependências podem ser instaladas.
RUN pip install --no-cache-dir -r requirements.txt


# ---- ESTÁGIO 2: A Imagem Final ----
# Começamos de novo com a imagem 'slim' limpa e leve para produção.
FROM python:3.11-slim

WORKDIR /app

# Copia o requirements.txt gerado no estágio 'builder'
COPY --from=builder /app/requirements.txt .

# Instala as dependências a partir do requirements.txt copiado.
# Este passo é geralmente muito mais rápido e confiável que o 'poetry install'.
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o resto do código da sua aplicação.
COPY . .

# Expõe a porta e define o comando de inicialização como antes.
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
