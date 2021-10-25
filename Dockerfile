FROM python:3.8-slim-buster

# update packages
RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN apt-get -qq update
RUN apt-get install --yes apache2 apache2-dev
WORKDIR /app

COPY ./requirements.txt .
RUN pip --use-deprecated=legacy-resolver install -r requirements.txt

COPY /DDI_Website /app


#unable to find python
# COPY docker-entrypoint.sh /docker-entrypoint.sh
# RUN chmod +x /docker-entrypoint.sh


COPY ./docker-entrypoint.sh /
ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
