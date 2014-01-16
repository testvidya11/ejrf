Installation
------------
* Postgres should be running and after cloning adjust localsettings.py accordingly for db setup 

##Git

        git clone https://github.com/eJRF/ejrf.git

        cd ejrf

        mkvirtualenv ejrf

        pip install -r pip-requirements.txt

        python manage.py syncdb --noinput

        python manage.py migrate

        python manage.py runserver
        
==

* run test and harvest

Done!! you're good to go :)

Filenaming convention:
* for tests: test_[[OBJECT]]_[[ACTION]].py
e.g: test_location_form.py, test_location_model.py, test_location_views.py

====

[![Build Status](https://travis-ci.org/eJRF/ejrf.png?branch=master)](https://travis-ci.org/eJRF/ejrf)
[![Coverage Status](https://coveralls.io/repos/eJRF/ejrf/badge.png)](https://coveralls.io/r/eJRF/ejrf)
