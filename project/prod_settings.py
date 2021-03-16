# file for storing sensitive data like passwords and secret key

SECRET_KEY = 'mt&+q9s5s)jk@0kw#_wb7q0#)n7mfa=fq#i^h!qc5#2ie2!h4j'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hagakure_db',
        'USER': 'postgres',
        'PASSWORD': 'iheartjudo',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_HOST_PASSWORD = 'iheartjudo'
