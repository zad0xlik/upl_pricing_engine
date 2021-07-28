FROM ubuntu:18.04

MAINTAINER FMK <fmk@fmk.com>

WORKDIR $HOME/irr

EXPOSE 5000
EXPOSE 8888
EXPOSE 6379
EXPOSE 9181

ENTRYPOINT [ "/bin/bash", "-c" ]

ARG PYTHON_VERSION_TAG=3.8.6
ARG LINK_PYTHON_TO_PYTHON3=1

RUN apt-get -qq -y update && \
    apt-get -qq -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
        gcc \
        g++ \
        zlibc \
        zlib1g-dev \
        libssl-dev \
        libbz2-dev \
        libsqlite3-dev \
        libncurses5-dev \
        libgdbm-dev \
        libgdbm-compat-dev \
        liblzma-dev \
        libreadline-dev \
        uuid-dev \
        libffi-dev \
        tk-dev \
        wget \
        curl \
        git \
        make \
        sudo \
        bash-completion \
        tree \
        vim \
        nano \
        net-tools \
        htop \
        postgresql-client \
        cron \
        software-properties-common \
        redis-server && \
    mv /usr/bin/lsb_release /usr/bin/lsb_release.bak && \
    apt-get -y autoclean && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt-get/lists/*

# install python
RUN cd /opt
COPY install_python.sh install_python.sh
RUN bash install_python.sh ${PYTHON_VERSION_TAG} ${LINK_PYTHON_TO_PYTHON3} && \
    rm -r install_python.sh Python-${PYTHON_VERSION_TAG}

COPY . $HOME/irr

RUN ls -la
RUN pwd

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN ["chmod", "+x", "proc_exec.sh"]

ARG ENV_BUILD
ARG PROJECT_NAME
ARG REDIS_URL

ENV ENV_BUILD $ENV_BUILD
ENV PROJECT_NAME $PROJECT_NAME
ENV REDIS_URL $REDIS_URL

CMD ["./proc_exec.sh"]