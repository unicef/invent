FROM node:12.21.0-alpine
# This is to allow npm to install from github
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD package.json /tmp/
RUN cd /tmp && npm i
RUN cd /usr/src/app && ln -s /tmp/node_modules

COPY . /usr/src/app/
RUN echo "NODE_ENV=production" >> .env
RUN npm build --quiet

# start command
CMD npm start

