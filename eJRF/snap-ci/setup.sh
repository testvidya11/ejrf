#!/bin/sh
cd ..
virtualenv ejrf_env
source ejrf_env/bin/activate
cd -
pip install -r pip-requirements.txt
pip install coveralls
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py
./manage.py syncdb --noinput
./manage.py migrate