FROM node:7.4

WORKDIR /app

COPY . /app
RUN npm install
RUN npm run tsc
RUN npm install -g http-server

EXPOSE 8080
CMD ["http-server", "-p", "8080", "-a", "0.0.0.0", "-d", "false"]
