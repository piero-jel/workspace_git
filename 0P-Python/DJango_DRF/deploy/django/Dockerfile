#imagen base
FROM python:3.11-slim

#copio el requirements
WORKDIR /projects
COPY ./requirements.txt /tmp/requirements.txt

#USER root

RUN apt-get update && apt-get --yes install apt-utils unzip
RUN apt-get install -y python3-pip 
RUN apt-get install -y vim
#RUN apt-get install -y postgresql postgresql-contrib
#RUN apt-get install -y python3-psycopg2
#RUN echo "alias python='python3'" >> /root/.bashrc
RUN apt-get install -y libpq-dev



#instalo los paquetes
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

## migramos, generamos la Base de datos
#RUN python3 manage.py migrate

#### BEGIN config deploy
#CMD ["gunicorn","--bind", "0.0.0.0:8000", "rd_wepapp.wsgi"]
#### END   config deploy
