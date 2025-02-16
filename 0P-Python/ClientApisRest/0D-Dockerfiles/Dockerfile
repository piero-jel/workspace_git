################################################################################
### BEGIN Copyright
# Copyright 2024, Jesus Emanuel Luccioni
# All rights reserved.
#
# This file is part of Docker Container Builds
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SCRIPT, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##
### END   Copyright
##########################################################################################################
#
# Version: 0.0.1
# FROM debian AS build_debian
# FROM ubuntu:kinetic AS build_debian
FROM python:3.12

LABEL author="JELuccioni"
LABEL email="jeluccioni@gmail.com"

ENV REFRESHED_AT 2024-05-16
LABEL version="1.0" location="Argentina" type="Dev Ops" role="Python3"

## BEGIN for python install locale module
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# es_AR UTF-8/es_AR UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG es_AR.UTF-8
ENV LC_NUMERIC es_AR.UTF-8
## END   for python install locale module


## -- creamos el directorio principal
WORKDIR /home/user
COPY bashrc.sh ./
COPY requerimientos.txt ./
#RUN mkdir -p /home/user

## set enviroment vars:
ENV LANG=es_AR LANGUAGE=es_AR.UTF-8
## FIXME
## for locale.Error: unsupported locale setting" on pip install
## equivalent export LC_ALL=C
ENV LC_ALL=C

## set alias, no funciona de esta forma
### BEGIN set alias in root files
RUN echo "alias cds='cd /home/user/'" >> /root/.bashrc
RUN cat bashrc.sh >> /root/.bashrc
RUN export PATH=$PATH:/home/user


### END

### BEGIN install packages python 
RUN apt-get update
RUN apt-get install -y python3-pip
RUN echo "alias python='python3'" >> /root/.bashrc

### END


## BEGIN Package for Python
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requerimientos.txt
## END   Package for Python


### BEGIN expose port and server 
# EXPOSE 8080
### END
