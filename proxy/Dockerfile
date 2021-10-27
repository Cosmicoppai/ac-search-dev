FROM nginx:1.21.3-alpine

COPY ./default.conf /etc/nginx/default.conf
COPY ./run.sh /run.sh

ENV HOST=${HOST}

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    mkdir -p /etc/letsencrypt && \
    chmod 755 /etc/letsencrypt && \
    mkdir -p /var/www/certbot && \
    chmod 755 /var/www/certbot && \
    touch /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh


VOLUME /vol/static
VOLUME /etc/letsencrypt
VOLUME /var/www/certbot

CMD ["/run.sh"]