# IE-0724-Proyecto-2

IE-0724 Laboratorio de Programacion Proyecto-2

## Miembros
- Marlon Lazo Coronado
- Jose Pablo Apú Picado

# Registry

Es una aplicación web para simular un registro de propiedades. Esta aplicación está escrita en python utiliza el framework Django.

## Instalar la base de datos
Instalar conda: https://docs.conda.io/en/latest/miniconda.html
Ya con conda instalado, cree un entorno virtual, activelo, y luego corra la aplicaión, con los siguiente comandos.
```sh
$ cd ./webapp
$ conda env create -f environment.yml
$ conda activate webapp
```

## Instalar la base de datos
Inicialice la base de datos.
```sh
$ python manage.py migrate
$ python manage.py createsuperuser
```

# Usos
Existen 2 formas de usar la aplicación
- Local
- Docker

## Correr la aplicación local
Ya con conda instalado y asegurnado que está en el entorno virtual webapp, corra la aplicación, con el siguiente comando.
```sh
$ python manage.py runserver
```

## Correr la aplicación en un contenedor de Docker
Instalar Docker: https://docs.docker.com/get-docker
Instalar Docker Compose: https://docs.docker.com/compose/install
Ya con Docker y Docker Compose instalados, basta con ejecutar el siguiente comando
```sh
$ docker-compose up --build
```