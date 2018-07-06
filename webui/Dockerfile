FROM nginx

EXPOSE 80

ENV NGINX_HOST="localhost"
ENV NGINX_PORT=80

COPY content /usr/share/nginx/html
RUN chmod -R o+rX /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
