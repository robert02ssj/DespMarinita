# Práctica 3.2 - Despliegue de WordPress con Docker y Docker Compose

## Descripción

En esta práctica se despliega un sitio **WordPress** en AWS usando contenedores Docker y Docker Compose, junto con MySQL, phpMyAdmin y HTTPS-PORTAL para habilitar acceso seguro por HTTPS.

## Pasos realizados

### Paso 1 - Crear instancia EC2 en AWS

Se crea una instancia EC2 con las siguientes características mínimas:

- **Tipo de instancia**: t2.small
- **Almacenamiento**: 20 GB
- **Puertos abiertos**: SSH (22/TCP), HTTP (80/TCP), HTTPS (443/TCP)

### Paso 2 - Instalar Docker y Docker Compose

```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

### Paso 3 - Crear los archivos de configuración

Se crea el archivo `.env` con todas las variables de entorno y el archivo `docker-compose.yml` con los cuatro servicios.

### Paso 4 - Desplegar los servicios

```bash
docker-compose up -d
docker-compose ps
```

### Paso 5 - Verificar el acceso

Se comprueba el acceso a WordPress desde el navegador usando la IP pública de la instancia y a phpMyAdmin en el puerto 8080.

### Paso 6 - Habilitar HTTPS

Se registra un dominio, se configuran los registros DNS y se actualiza la variable `DOMAIN` en el `.env`. Finalmente se reinician los servicios:

```bash
docker-compose down && docker-compose up -d
```

## Descripción del archivo docker-compose.yml

El archivo define cuatro servicios organizados en dos redes:

**frontend-network**: `wordpress`, `phpmyadmin`, `https-portal`  
**backend-network**: `mysql`

El servicio `mysql` no expone puertos al host, solo es accesible desde la red interna.

| Servicio | Imagen | Red | Puerto |
|---|---|---|---|
| `mysql` | mysql | backend-network | — (interno) |
| `wordpress` | bitnami/wordpress | frontend + backend | — |
| `phpmyadmin` | phpmyadmin/phpmyadmin | frontend + backend | 8080 |
| `https-portal` | steveltn/https-portal:1 | frontend-network | 80, 443 |

El servicio `mysql` incluye un `healthcheck` para garantizar que está listo antes de que arranque WordPress. Se usa `depends_on` con `condition: service_healthy` para controlar el orden de inicio.

Todos los servicios tienen `restart: always` para que se reinicien automáticamente ante fallos.

Las variables de entorno se cargan desde el archivo `.env`.

## URL del repositorio de GitHub

> Sustituir por la URL real del repositorio de GitHub donde se aloje esta práctica.

## URL del sitio web con HTTPS habilitado

> Sustituir por la URL real del sitio web con HTTPS habilitado.
