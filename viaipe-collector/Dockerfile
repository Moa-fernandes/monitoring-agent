FROM python:3.12

WORKDIR /app
COPY . .

# Adiciona o cliente do PostgreSQL dentro do container
RUN apt-get update && apt-get install -y postgresql-client

RUN pip install -r requirements.txt

CMD ["python", "collector.py"]
