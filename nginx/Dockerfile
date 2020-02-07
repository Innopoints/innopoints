FROM nginx:1.14-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.docker.conf /etc/nginx/nginx.conf

EXPOSE 80
