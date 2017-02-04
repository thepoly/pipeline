FROM node:6

RUN apt-get update \
	&& apt-get install --no-install-recommends --no-install-suggests -y nginx \
	&& rm -rf /var/lib/apt/lists/*

# forward nginx logs to docker logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /app
ADD ./package.json /app
RUN npm install

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY . /app

EXPOSE 80
CMD ["sh", "/app/web.sh"]
