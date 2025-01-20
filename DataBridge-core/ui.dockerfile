FROM node:23

EXPOSE 3000:3000/tcp

RUN apt-get install -y git

RUN adduser databridge

USER databridge

RUN git clone https://github.com/databridge-org/databridge-core.git /home/databridge/src

WORKDIR /home/databridge/src/ui-component

RUN npm run build &\
    npm start