FROM ubuntu:latest

RUN \
    apt-get update && \
    apt-get install -y wget python3 python3-pip python3-dev &&\
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /data

ENTRYPOINT ["gunicorn", "-w 2", "-b 0.0.0.0:5000", "servidor:app"]