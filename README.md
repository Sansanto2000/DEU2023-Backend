# DEU2023-Backend

Para levantar los contenedores ejecutar el comando `docker-compose up`.

## Tutorial usado:
https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

## Comandos (Dev)

Tirar abajo contenedores:
```
docker-compose down -v
```
Construir imagen y Ejecutar:
```
docker-compose up -d --build
```

Checkear ejecucion en `http://localhost:5001`

En DEV la base de datos se crea e inicializa de forma automatica con cada ejecución.

## Comandos (Prod)

### Tirar abajo contenedores
```
docker-compose -f docker-compose.prod.yml down -v
```
### Construir imagen y Ejecutar
```
docker-compose -f docker-compose.prod.yml up -d --build
```
Checkear ejecucion en `http://localhost:1337`

### Reiniciar DB
```
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
```


## Visualizacion de los datos de la DB

Los datos de la DB se pueden checkear haciendo uso del siguiente comando:
```
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
```
Esto te dara una consola para interactuar con la DB.

Comandos utiles:
- listar DBs: `\l`
- conectar con DBs de app: `\c hello_flask_dev`
- (una vez conectado) listar tablas: `\dt`
- (una vez conectado) listar elementos de tabla: `select * from {nombre_tabla};` Ejemplo: `select * from users;`
- (una vez conectado) desconectar consola: `\q`