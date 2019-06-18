FROM ubuntu:18.04
RUN apt-get update
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN ln -fs /usr/share/zoneinfo/Europe/London /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get install -y wget gnupg python3-dev python3-venv curl git ssh tar gzip ca-certificates
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
RUN curl -sS https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" | tee /etc/apt/sources.list.d/postgresql.list
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update
RUN apt-get install -y nodejs
RUN apt-get install -y build-essential yarn postgresql-10 redis-server
COPY --chown=postgres:postgres  pg_hba.conf /etc/postgresql/10/main
RUN chmod 644 /etc/postgresql/10/main/pg_hba.conf
COPY --chown=redis:redis  redis.conf /etc/redis/
RUN chmod 640 /etc/redis/redis.conf
