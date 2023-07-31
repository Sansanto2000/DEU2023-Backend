# pull official base image
FROM python:3.11.3-slim-buster

# set work directory
WORKDIR /usr/src/app

# Generar los certificados autofirmados
# RUN openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -subj '/CN=localhost' -keyout key.pem -out cert.pem

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Variables de configuracion de conexion a PostgresDB
ENV FLASK_APP=project/__init__.py
ENV FLASK_DEBUG=1
ENV DATABASE_URL=postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev
ENV SQL_HOST=db
ENV SQL_PORT=5432
ENV DATABASE=postgres
ENV APP_FOLDER=/usr/src/app

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

EXPOSE 5000

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD "python manage.py run -h 0.0.0.0"