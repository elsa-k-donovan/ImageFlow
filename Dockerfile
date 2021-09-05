FROM python:3.8-slim-buster

# update packages
RUN apt-get -qq update
RUN apt-get install --yes apache2 apache2-dev

WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
