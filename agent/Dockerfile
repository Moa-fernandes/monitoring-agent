# Usando Python como base
FROM python:3.12

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando os arquivos do projeto para dentro do container
COPY . .

# Instalando as dependências
RUN pip install -r requirements.txt

# Definindo o comando padrão
CMD ["python", "monitor.py"]
