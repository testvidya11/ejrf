#!/bin/sh
source ../ejrf_env/bin/activate
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py
./manage.py syncdb --noinput
./manage.py migrate
./manage.py test