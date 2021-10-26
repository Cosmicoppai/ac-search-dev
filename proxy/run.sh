#!/bin/sh

set -e

envsubst '${HOST}' < /etc/nginx/default.conf > /etc/nginx/conf.d/default.conf

while :; do sleep 6h && wait $$/\{!/\}; nginx -s reload; done & nginx -g "daemon off;"