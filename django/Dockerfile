FROM python:3.7-stretch

RUN apt-get update && apt-get install -y gettext  # django i18n needs this
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g mapshaper

RUN mkdir /src
WORKDIR /src
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD . /src/