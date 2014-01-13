DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ejrf",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "localhost",
    }
}

LETTUCE_AVOID_APPS = (
        'south',
        'django_nose',
        'lettuce.django',
        'django_extensions',
        'bootstrap_pagination',
)
