# Práctica 4 - CI/CD con GitHub Actions, Docker Hub y Flask

## Descripción

En esta práctica se implementa un pipeline de **CI/CD** (Integración Continua y Despliegue Continuo) para una aplicación web desarrollada con **Flask**. El pipeline automatiza la ejecución de tests unitarios y la publicación de la imagen Docker en Docker Hub cada vez que se realiza un `push` a la rama `main`.

## Conceptos clave

- **CI (Integración Continua)**: integrar en el repositorio los nuevos cambios del código fuente y ejecutar tests automáticamente.
- **CD (Entrega/Despliegue Continuo)**: automatizar la generación del artefacto (imagen Docker) y su publicación en un registro.
- **Pipeline**: conjunto de pasos automatizados que se ejecutan en orden.

## Estructura del proyecto

```
practica-4/
├── src/
│   └── app.py                        # Aplicación Flask
├── tests/
│   └── test_app.py                   # Tests unitarios
├── .github/
│   └── workflows/
│       └── ci-cd.yml                 # Pipeline de GitHub Actions
├── Dockerfile                        # Imagen Docker de la aplicación
├── docker-compose.yml                # Despliegue local con Docker Compose
├── requirements.txt                  # Dependencias Python
└── README.md
```

## Pasos realizados

### Paso 1 - Crear la aplicación Flask

Se crea la aplicación en `src/app.py` con dos rutas:
- `/` → responde con "Hola Mundo"
- `/about` → responde con "Acerca de"

### Paso 2 - Escribir los tests unitarios

Se crean en `tests/test_app.py` tests unitarios con `unittest` que comprueban que las rutas devuelven el código de estado 200.

Para ejecutar los tests localmente:

```bash
python3 -m unittest tests/*.py
```

### Paso 3 - Crear el Dockerfile

Se conteneriza la aplicación Flask usando `python:3.13-alpine` como imagen base ligera.

### Paso 4 - Configurar GitHub Actions

Se crea el archivo `.github/workflows/ci-cd.yml` con dos jobs:

1. **test**: instala dependencias y ejecuta los tests unitarios.
2. **build-and-push**: solo se ejecuta si los tests pasan. Construye la imagen Docker y la publica en Docker Hub con la etiqueta `latest` y el SHA del commit.

### Paso 5 - Configurar secretos en GitHub

En el repositorio de GitHub → Settings → Secrets se añaden:
- `DOCKERHUB_USERNAME`: nombre de usuario de Docker Hub
- `DOCKERHUB_TOKEN`: token de acceso de Docker Hub

### Paso 6 - Desplegar en AWS

Se crea una instancia EC2, se instala Docker y Docker Compose y se despliega la imagen publicada:

```bash
docker-compose up -d
```

## Descripción del pipeline CI/CD

El archivo `.github/workflows/ci-cd.yml` define el siguiente flujo:

```
push a main
    │
    ▼
[Job: test]
    ├── Checkout del código
    ├── Configurar Python 3.13
    ├── Instalar dependencias (pip install)
    └── Ejecutar tests unitarios
    │
    ▼ (solo si tests pasan)
[Job: build-and-push]
    ├── Checkout del código
    ├── Login en Docker Hub
    └── Build y push de la imagen con etiquetas latest y SHA
```

El job `build-and-push` depende de `test` mediante `needs: test`, garantizando que nunca se publique una imagen que no pase los tests.

## URL del repositorio de GitHub

> Sustituir por la URL real del repositorio de GitHub donde se aloje esta práctica.
