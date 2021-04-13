FROM ubuntu:latest

# Python
RUN \
    apt-get update && \
    apt-get install -y wget python3 python3-pip python3-dev virtualenv vim &&\
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt install htop

RUN ln -s /bin/pip3 /bin/pip

# requitements.txt
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN ln -s /bin/python3 /bin/python

WORKDIR /data

CMD ["bash"]