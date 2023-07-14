FROM alpine:3.17

RUN apk add --no-cache python3-dev py3-build py3-setuptools

WORKDIR /heterocl
COPY . .
RUN python3 -m build --wheel -o ./dist .

CMD install --mode=666 -Dt /dist /heterocl/dist/* 
