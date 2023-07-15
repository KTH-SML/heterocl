FROM ubuntu:22.04 

RUN apt-get update && \
    apt-get install -y \
      python3-dev  \
      python3-build \
      python3-virtualenv \
      python3-setuptools \
      && \
    rm -r /var/lib/apt/lists/*

WORKDIR /heterocl
COPY . .
RUN python3 -m build --wheel -o ./dist .

CMD install --mode=666 -Dt /dist /heterocl/dist/* 
