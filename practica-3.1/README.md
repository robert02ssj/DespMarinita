# Práctica 3.1 - HTTPS con Let's Encrypt, Docker y Docker Compose

## Descripción

En esta práctica se habilita el protocolo HTTPS en un sitio web **PrestaShop** desplegado con contenedores Docker en una instancia EC2 de AWS, utilizando certificados gratuitos de **Let's Encrypt** a través de la imagen **HTTPS-PORTAL**.

## Pasos realizados

### Paso 1 - Crear instancia EC2 en AWS

Se crea una instancia EC2 con las siguientes características mínimas:

- **Tipo de instancia**: t2.small
- **Almacenamiento**: 20 GB
- **Puertos abiertos**: SSH (22/TCP), HTTP (80/TCP), HTTPS (443/TCP)

### Paso 2 - Obtener la dirección IP pública

Una vez creada la instancia, se anota la dirección IP pública asignada desde la consola de AWS.

### Paso 3 - Registrar un nombre de dominio

Se registra un dominio gratuito en un proveedor como [Freenom](http://www.freenom.com/).

### Paso 4 - Configurar los registros DNS

En el panel de control del proveedor de dominio se crean dos registros de tipo A apuntando a la IP pública de la instancia EC2:

- Registro A sin prefijo → IP pública EC2
- Registro A `www` → IP pública EC2

Se puede comprobar la propagación en [dnschecker.org](https://dnschecker.org/).

### Paso 5 - Instalar Docker y Docker Compose

```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

### Paso 6 - Configurar y desplegar los servicios

Se modifica el archivo `.env` con el dominio registrado y se despliegan los servicios:

```bash
docker-compose up -d
```

## Descripción del archivo docker-compose.yml

El archivo define cuatro servicios:

| Servicio | Imagen | Red | Descripción |
|---|---|---|---|
| `mysql` | mysql:9.1 | backend-network | Base de datos de PrestaShop |
| `phpmyadmin` | phpmyadmin:5.2.1 | backend + frontend | Gestor visual de la BD (puerto 8080) |
| `prestashop` | prestashop/prestashop:8 | backend + frontend | Tienda online |
| `https-portal` | steveltn/https-portal:1 | frontend-network | Proxy inverso con certificado SSL automático |

**HTTPS-PORTAL** actúa como proxy inverso: recibe las peticiones en los puertos 80 y 443 y las redirige al contenedor de PrestaShop. El certificado SSL lo obtiene y renueva automáticamente desde Let's Encrypt.

La variable `STAGE` puede tomar los valores:
- `local` → certificado autofirmado (pruebas locales)
- `staging` → certificado de prueba de Let's Encrypt
- `production` → certificado válido de Let's Encrypt

## URL del repositorio de GitHub

> Sustituir por la URL real del repositorio de GitHub donde se aloje esta práctica.

## URL del sitio web con HTTPS habilitado

> Sustituir por la URL real del sitio web con HTTPS habilitado.
