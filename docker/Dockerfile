FROM hcl-dialect AS hcl-dialect

FROM ubuntu:22.04 

COPY --from=hcl-dialect /dist /dist

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
RUN python3 -m build --wheel -o ./dist . && \
    install --mode=666 -Dt /dist ./dist/* 
