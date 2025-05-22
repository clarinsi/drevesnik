#!/bin/sh

# Automatically substitute environment variable into the template
envsubst '${WWW_ADDRESS_POSTFIX}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/nginx.conf

# Start nginx in foreground
exec nginx -g 'daemon off;'
