FROM nginx:1.14-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.common.conf /etc/nginx/
COPY nginx.dev.conf /etc/nginx/nginx.conf

EXPOSE 80
