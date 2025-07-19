# Dockerfile (Corrigido)
FROM python:3.11-slim

# Instala as ferramentas de compilação C/C++ necessárias
# para bibliotecas como pandas e scikit-learn.
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
