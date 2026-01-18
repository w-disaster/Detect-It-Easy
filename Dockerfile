FROM ubuntu:24.04

RUN apt update -qq && apt upgrade -y  && apt install -y wget && \
    # Beta version needed to support recent signatures
    wget https://github.com/horsicq/DIE-engine/releases/download/Beta/die_3.11_Ubuntu_24.04_amd64.deb  && \
    apt install -y ./die_3.11_Ubuntu_24.04_amd64.deb && \
    rm die_3.11_Ubuntu_24.04_amd64.deb && rm -rf /usr/lib/die/db && \
    # These are needed for poetry
    apt install -y curl openssl

# db update
COPY ./db /usr/lib/die/db

COPY ./entrypoint.py /usr/bin/entrypoint.py

RUN mkdir /usr/dataset/
ENV BASE_BIN_DIR="/usr/dataset/"
ENV DIEC_RESULTS_FILENAME="/usr/results/"

WORKDIR /usr/app
COPY . .

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry install --no-root

ENTRYPOINT ["poetry", "run", "python3", "/usr/bin/entrypoint.py"]
