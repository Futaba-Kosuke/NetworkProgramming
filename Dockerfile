FROM ubuntu:16.04

RUN apt update && \
    apt install -y build-essential vim
