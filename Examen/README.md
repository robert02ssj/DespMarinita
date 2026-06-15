# Examen DAW - Segunda Evaluación - Recuperación 2025/2026

## Estructura del repositorio

```
├── README.md
├── capturas
└── docker
    ├── Dockerfile
    └── docker-compose.yml
```

---

## Ejercicio 1. GitHub (0,5 puntos)

Se ha creado el repositorio privado `examen-daw-2-eval` en GitHub y se ha añadido al profesor como colaborador.

**Capturas de pantalla:**

> Añadir captura de la creación del repositorio y del colaborador añadido.

---

## Ejercicio 2. Creación de la infraestructura en AWS (0,5 puntos)

### Grupo de seguridad

Se crea el grupo de seguridad `grupo_seguridad_ejercicio_2` con las siguientes reglas:

| Tipo  | Puerto | Protocolo | Source    |
|-------|--------|-----------|-----------|
| SSH   | 22     | TCP       | 0.0.0.0/0 |
| HTTP  | 80     | TCP       | 0.0.0.0/0 |
| HTTPS | 443    | TCP       | 0.0.0.0/0 |

Reglas de salida: todo el tráfico hacia 0.0.0.0/0.

### Instancia EC2

| Campo              | Valor                     |
|--------------------|---------------------------|
| Nombre             | instancia_ejercicio_2     |
| AMI                | Ubuntu 24.04 LTS          |
| Tipo de instancia  | t2.medium                 |
| Key pair           | vockey                    |
| Grupo de seguridad | grupo_seguridad_ejercicio_2 |

### Script de instalación de Docker y Docker Compose

```bash
#!/bin/bash

# Actualizar el sistema
apt-get update -y
apt-get upgrade -y

# Instalar Docker
apt-get install -y docker.io

# Habilitar e iniciar Docker
systemctl enable docker
systemctl start docker

# Instalar Docker Compose
apt-get install -y docker-compose

# Añadir el usuario ubuntu al grupo docker
usermod -aG docker ubuntu
```

**Comandos para ejecutar el script en la instancia:**

```bash
# Copiar el script a la instancia
scp -i vockey.pem install_docker.sh ubuntu@<IP_PUBLICA>:~

# Conectarse a la instancia
ssh -i vockey.pem ubuntu@<IP_PUBLICA>

# Ejecutar el script
sudo bash install_docker.sh

# Comprobar que Docker funciona
docker --version
docker-compose --version
```

**Capturas de pantalla:**

> Añadir captura de la creación del grupo de seguridad.
> Añadir captura de la instancia EC2 creada.
> Añadir captura de la ejecución del script y verificación de Docker instalado.

---

## Ejercicio 3. Docker (1,5 puntos)

Se ha creado el archivo `docker/Dockerfile` para construir una imagen con **Nginx** que sirve la web estática del repositorio [floppybird](https://github.com/nebez/floppybird).

### Dockerfile

```dockerfile
FROM debian:latest

RUN apt-get update && apt-get install -y \
    nginx \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/nebez/floppybird /var/www/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

- Imagen base: `debian:latest`
- Se instalan `nginx` y `git` en una sola capa RUN.
- Se clona el repositorio de floppybird en `/var/www/html/`, directorio raíz de Nginx.
- Nginx arranca en primer plano con `daemon off`.

### Comandos utilizados

```bash
# Construir la imagen
docker build -t floppybird ./docker

# Comprobar que la imagen se ha creado
docker images

# Crear un contenedor de prueba
docker run -d -p 80:80 --name test-floppybird floppybird

# Comprobar que el contenedor está en ejecución
docker ps

# Parar y eliminar el contenedor de prueba
docker stop test-floppybird
docker rm test-floppybird
```

**Capturas de pantalla:**

> Añadir captura de `docker build`.
> Añadir captura de `docker images`.
> Añadir captura del navegador mostrando la web floppybird.

---

## Ejercicio 4. Publicar imagen en Docker Hub con GitHub Actions (1,5 puntos)

Se ha configurado GitHub Actions en el archivo `.github/workflows/docker-publish.yml` para que en cada `push` a la rama `main` se construya la imagen Docker y se publique automáticamente en Docker Hub.

### Secretos configurados en GitHub

En **Settings → Secrets and variables → Actions** se han añadido:

| Secret              | Valor                              |
|---------------------|------------------------------------|
| `DOCKERHUB_USERNAME` | Nombre de usuario de Docker Hub   |
| `DOCKERHUB_TOKEN`   | Token de acceso de Docker Hub      |

### Flujo del pipeline

```
push a main
    │
    ▼
[Job: build-and-push]
    ├── Checkout del repositorio
    ├── Login en Docker Hub
    └── Build y push con etiquetas latest y SHA del commit
```

### Comandos para verificar localmente antes del push

```bash
# Añadir los archivos al repositorio
git add .
git commit -m "Añadir Dockerfile y configuración de GitHub Actions"
git push origin main
```

**Capturas de pantalla:**

> Añadir captura del workflow ejecutándose en GitHub Actions.
> Añadir captura de la imagen publicada en Docker Hub.

---

## Ejercicio 5. Docker Compose (1 punto)

Se ha creado el archivo `docker/docker-compose.yml` con dos servicios:

1. **web**: contenedor creado a partir de la imagen publicada en Docker Hub en el ejercicio anterior.
2. **https-portal**: proxy inverso que gestiona el certificado SSL/TLS de Let's Encrypt automáticamente.

### Dominio utilizado

Se utiliza el servicio **nip.io** como DNS wildcard. El dominio tiene el formato `<IP_PUBLICA>.nip.io`, por ejemplo: `1.2.3.4.nip.io`.

### Variables de entorno necesarias

Crear un archivo `.env` junto al `docker-compose.yml`:

```bash
DOCKERHUB_USERNAME=<tu_usuario_dockerhub>
DOMAIN=<IP_PUBLICA>.nip.io
```

### Comandos utilizados

```bash
# Desplegar los servicios
docker-compose -f docker/docker-compose.yml up -d

# Comprobar que los servicios están en ejecución
docker-compose -f docker/docker-compose.yml ps

# Ver los logs de https-portal para verificar el certificado
docker-compose -f docker/docker-compose.yml logs https-portal
```

**Capturas de pantalla:**

> Añadir captura de `docker-compose ps` con los servicios activos.
> Añadir captura del navegador mostrando la web floppybird con HTTPS habilitado (candado verde).
