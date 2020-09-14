FROM nginx:1.15
LABEL maintainer="web@poly.rpi.edu"

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir /var/log/nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
