FROM alpine:latest

COPY dirb.sh /app/dirb.sh
COPY common.txt /app/common.txt
COPY ffuf /bin/ffuf

ARG GIT_USERNAME
ARG GIT_PASSWORD

ENV GIT_USERNAME=${GIT_USERNAME}
ENV GIT_PASSWORD=${GIT_PASSWORD}

RUN apk update && apk add git

WORKDIR /app

ENTRYPOINT ["/bin/sh", "/app/dirb.sh"]

