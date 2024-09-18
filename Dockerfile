# Escolhendo a imagem base
FROM python:3.10-slim

# Definindo o diretório de trabalho no contêiner
WORKDIR /app

# Copiando o arquivo de requisitos
COPY requirements.txt /app/

# Instalando as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiando o restante dos arquivos da aplicação
COPY . /app

# Rodando as migrações do banco de dados
# Executando o comando RUN a nível de buildar o container
# RUN python manage.py migrate
RUN pip install django Pillow django-crispy-forms crispy-bootstrap5 psycopg2-binary

# Expondo a porta em que a aplicação rodará
EXPOSE 8200

# Comando para iniciar a aplicação
# O comando CMD (comand) será executado após buildar o docker
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8200"]

# Instruções adicionais:
# Para construir a imagem Docker: `docker build -t cityhub .`
# Para rodar a imagem passando o comando -p para mapear as portas: `docker run -p 8200:8200 cityhub`
