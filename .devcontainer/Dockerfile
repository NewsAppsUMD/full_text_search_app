# This Dockerfile is used to build a Python 3.10 development container with necessary packages and FTS5-enabled SQLite

# Base image: Python 3.10 from Microsoft's Visual Studio Code development container repository
FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install necessary packages
# apt-get update: Update the package list
# apt-get install -y wget gcc make: Install wget, gcc, and make with the "-y" flag to automatically accept any prompts
RUN apt-get update && apt-get install -y wget gcc make

# Install Python libraries: peewee (ORM for SQLite) and Flask (web framework)
RUN pip install peewee Flask

# Download the SQLite source code from the official website, and extract it using tar
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3410200.tar.gz && \
    tar -zxvf sqlite-autoconf-3410200.tar.gz

# Set the working directory to the extracted SQLite source code folder
WORKDIR sqlite-autoconf-3410200

# Build and install SQLite with FTS5 (full-text search) enabled
# ./configure --enable-fts5: Configure the build with FTS5 enabled
# sudo make: Build SQLite
# sudo make install: Install the built SQLite
RUN ./configure --enable-fts5 && \
    sudo make && \
    sudo make install
