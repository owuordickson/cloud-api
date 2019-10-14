FROM nginx:alpine
COPY angularjs_app /var/www/html
COPY docker-entrypoint.sh /etc/nginx/docker-entrypoint.sh
RUN chmod +x /etc/nginx/docker-entrypoint.sh
ENTRYPOINT ["/etc/nginx/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
