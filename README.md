# DEU2023-Backend

Para levantar los contenedores ejecutar el comando `docker-compose up`.

## Tutorial usado:
https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

## Comandos (Dev)

### Tirar abajo contenedores
```
docker-compose down -v
```
### Construir imagen
```
docker-compose up -d --build
```

### Ejecutar
```
docker-compose exec web python manage.py create_db
```
Checkear ejecucion en `http://localhost:5001`

## Comandos (Prod)

### Tirar abajo contenedores
```
docker-compose -f docker-compose.prod.yml down -v
```
### Construir imagen
```
docker-compose -f docker-compose.prod.yml up -d --build
```

### Ejecutar
```
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
```
Checkear ejecucion en `http://localhost:1337`


## Visualizacion de datos

Los datos de la DB se visualizan desde pgadmin, accesible desde `localhost:80`.
