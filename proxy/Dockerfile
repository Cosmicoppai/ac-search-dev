FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf /etc/nginx/default.conf
COPY ./run.sh /run.sh

ENV HOST=${HOST}

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    mkdir -p /etc/letsencrypt && \
    chmod 755 /etc/letsencrypt && \
    mkdir -p /var/www/certbot && \
    chmod 755 /var/www/certbot && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/letsencrypt/ && \
    chown nginx:nginx /var/www/certbot/ && \
    chmod +x /run.sh


VOLUME /vol/static
VOLUME /etc/letsencrypt
VOLUME /var/www/certbot

USER nginx

CMD ["/run.sh"]