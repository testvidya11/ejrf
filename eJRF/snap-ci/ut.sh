#!/bin/sh
source ../ejrf_env/bin/activate
./manage.py syncdb --noinput
./manage.py migrate
./manage.py test