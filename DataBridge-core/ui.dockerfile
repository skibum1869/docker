FROM ubuntu:latest

EXPOSE 3000:3000/tcp

# Install build dependencies
RUN apt-get clean \
    && apt-get update \
    && apt-get install -y git npm

# Copy ui scripts
COPY ./ui/ ~/ui

RUN cd ~/ui/ & \
    npm run build \
    npm start