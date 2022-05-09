FROM nginx

COPY uwsgi_params /etc/nginx/uwsgi_params

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir -p /vol/nginx
RUN chmod 755 /vol/nginx