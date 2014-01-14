#!/bin/sh
virtualenv ejrf_env
source ejrf_env/bin/activate
pip install -r pip-requirements.txt
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py
