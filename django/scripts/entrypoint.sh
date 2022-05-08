#!/bin/sh

set -e

cd && cd /django/django_client/

uwsgi --ini /etc/django.ini