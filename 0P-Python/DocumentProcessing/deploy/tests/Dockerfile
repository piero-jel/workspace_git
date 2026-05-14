FROM python:3.14-slim

# copiamos system/pip dependencies
COPY ./tests/system_dependencies.txt /tmp/system_dependencies.txt
COPY ./tests/pip_requirements.txt /tmp/requirements.txt


# Actualizar paquetes e instalar dependencias necesarias
# Install system dependencies (e.g., for psycopg2 if using PostgreSQL)
RUN apt-get update && apt-get install -y $(cat /tmp/system_dependencies.txt) \
    && rm -rf /var/lib/apt/lists/*


# Instalacion de los paquetes
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Establecemos el volumen donde tendremos la informacion
WORKDIR /application

# Create a non-root user for security
RUN useradd -m appuser
USER appuser
