#imagen base
FROM postgres:14.5

# RUN apt-get install -y libpq-dev
# RUN apt-get install -y postgresql postgresql-contrib
# RUN apt-get install -y vim


### BEGIN comandos a ejecutar al inicio del contendor
CMD service postgresql start
CMD su - postgres &&\
    psql -c "ALTER USER postgres PASSWORD '12345';" &&\
    psql -c "CREATE DATABASE items;" &&\
    exit
### END
#### END   config deploy
#
