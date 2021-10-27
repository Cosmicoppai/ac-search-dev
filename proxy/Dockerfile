FROM nginx:1.21.3-alpine

COPY ./default.conf /etc/nginx/default.conf
COPY ./run.sh /run.sh

ENV HOST=${HOST}

CMD ["/run.sh"]