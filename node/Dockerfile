FROM node:12.16.1-alpine
RUN mkdir /opt/djreact
RUN npm install -g serve
WORKDIR /opt/djreact
COPY ./package.json /opt/djreact/package.json
RUN npm install package.json
