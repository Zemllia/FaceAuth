FROM python:3.8.2-slim

WORKDIR /app

# set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get install cmake build-essential cmake pkg-config libx11-dev libatlas-base-dev \
     libgtk-3-dev libboost-python-dev postgresql postgresql-contrib libpq-dev libglib2.0-0 -y

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -U pip wheel cmake
RUN pip install -r requirements.txt

# Copy Project

COPY . .
