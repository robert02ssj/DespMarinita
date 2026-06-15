# Práctica 3.4 - «Dockerizar» una web estática y publicarla en Docker Hub

## Descripción

En esta práctica se crea una imagen Docker con la aplicación web estática [2048](https://github.com/josejuansanchez/2048), servida con Nginx. La imagen se publica en Docker Hub y se automatiza la publicación con GitHub Actions. Finalmente se despliega en una instancia EC2 de AWS.

## Pasos realizados

### Paso 1 - Crear el archivo Dockerfile

Se crea el archivo `Dockerfile` con los requisitos indicados:

- Imagen base: `ubuntu:latest`
- Se instala Nginx y Git
- Se clona el repositorio de la aplicación 2048 en `/var/www/html/`
- Se expone el puerto 80
- Comando de inicio: `CMD ["nginx", "-g", "daemon off;"]`

### Paso 2 - Construir la imagen localmente

```bash
docker build -t nginx-2048 .
docker images
```

### Paso 3 - Etiquetar la imagen con el usuario de Docker Hub

```bash
docker tag nginx-2048 <usuario>/nginx-2048:1.0
docker tag nginx-2048 <usuario>/nginx-2048:latest
```

### Paso 4 - Publicar la imagen en Docker Hub

```bash
docker login
docker push <usuario>/nginx-2048:1.0
docker push <usuario>/nginx-2048:latest
```

### Paso 5 - Crear instancia EC2 y desplegar

Se crea una instancia EC2 en AWS, se instala Docker y Docker Compose y se despliega la aplicación:

```bash
docker-compose up -d
```

### Paso 6 - Automatizar la publicación con GitHub Actions

Se configura el archivo `.github/workflows/docker-publish.yml` para que en cada `push` a la rama `main` se construya y publique la imagen automáticamente en Docker Hub.

Se crean dos secretos en el repositorio de GitHub:
- `DOCKERHUB_USERNAME`: nombre de usuario de Docker Hub
- `DOCKERHUB_TOKEN`: token de acceso generado en Docker Hub (sección Security)

## Descripción del Dockerfile

```dockerfile
FROM ubuntu:latest

RUN apt-get update && apt-get install -y nginx git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/josejuansanchez/2048 /var/www/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

- Se parte de `ubuntu:latest` como imagen base.
- Se instalan Nginx y Git en una sola capa RUN para minimizar el tamaño de la imagen.
- Se clona el juego 2048 directamente en el directorio raíz de Nginx.
- Nginx arranca en primer plano para que Docker pueda controlar el proceso.

## Descripción de las acciones realizadas

La imagen se construyó localmente, se etiquetó con las versiones `1.0` y `latest` y se publicó en Docker Hub. Se configuró GitHub Actions para automatizar este proceso en cada `push` a la rama `main`. La aplicación web se desplegó en EC2 usando `docker-compose.yml` que referencia la imagen publicada en Docker Hub.

## URL del repositorio de GitHub

> Sustituir por la URL real del repositorio de GitHub donde se aloje esta práctica.
