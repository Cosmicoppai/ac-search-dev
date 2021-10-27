#!/bin/sh

set -e

envsubst '${HOST}' < /etc/nginx/default.conf > /etc/nginx/conf.d/default.conf