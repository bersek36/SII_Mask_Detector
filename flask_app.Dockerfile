FROM ubuntu:latest

RUN \
    apt-get update && \
    apt-get install -y wget python3 python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get -y install ffmpeg libsm6 libxext6

COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /data

ENTRYPOINT cd download_from_google && \
           python3 download_models.py && \
           cd .. && \
           gunicorn -w 2 -b 0.0.0.0:5000 servidor:app