FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install necessary packages
RUN apt-get update && apt-get install -y wget gcc make

RUN pip install peewee Flask

# Download SQLite source code and extract it
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3410200.tar.gz && \
    tar -zxvf sqlite-autoconf-3410200.tar.gz

# Build SQLite with FTS5 enabled
WORKDIR sqlite-autoconf-3410200
RUN ./configure --enable-fts5 && \
    sudo make && \
    sudo make install