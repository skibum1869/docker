FROM ubuntu:latest

EXPOSE 3000:3000/tcp

# Install build dependencies
RUN apt-get clean \
    && apt-get update

RUN apt-get install -y git npm

RUN git clone https://github.com/databridge-org/databridge-core.git /opt/databridge

RUN cd /opt/databridge/ui-component/ & \
    npm install & \
    npm run build & \
    npm start