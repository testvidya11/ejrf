#!/bin/sh
curl $GIST_URL | bash
source ../ejrf_env/bin/activate
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py
cp eJRF/snap-ci/initial_steps.py questionnaire/features/initial_steps.py
./manage.py harvest