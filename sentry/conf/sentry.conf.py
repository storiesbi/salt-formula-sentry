{%- from "sentry/map.jinja" import server with context %}

import os.path

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # We suggest PostgreSQL for optimal performance
        'NAME': '{{ server.database.name }}',
        'USER': '{{ server.database.user }}',
        'PASSWORD': '{{ server.database.password }}',
        'HOST': '{{ server.database.host }}',
        'PORT': '5432',
    }
}

# If you're expecting any kind of real traffic on Sentry, we highly recommend configuring
# the CACHES and Redis settings

SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

CELERY_ALWAYS_EAGER = False

SECRET_KEY = '{{ server.secret_key }}'

# You should configure the absolute URI to server. It will attempt to guess it if you don't
# but proxies may interfere with this.
{%- if server.bind.name is defined %}
SENTRY_URL_PREFIX = 'http://{{ server.bind.name }}'
{%- else %}
{%- if pillar.nginx.proxy is defined %}
SENTRY_URL_PREFIX = 'http://{{ server.bind.name }}'
{%- else %}
SENTRY_URL_PREFIX = 'http://{{ server.bind.url }}:{{ server.bind.port }}'
{%- endif %}
{%- endif %}

ALLOWED_HOSTS = [
    '*',
]

SENTRY_REMOTE_TIMEOUT = 10

SENTRY_REMOTE_URL = 'http://{{ server.bind.name }}/sentry/store/'

SENTRY_WEB_HOST = '{{ server.bind.address }}'
SENTRY_WEB_PORT = {{ server.bind.port }}
SENTRY_WEB_OPTIONS = {
    'workers': {{ server.get('workers', '3') }},  # the number of gunicorn workers
#    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},  # detect HTTPS mode from X-Forwarded-Proto header
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Mail server configuration

{%- if server.broker is defined and server.broker.engine == 'redis' %}
BROKER_URL = 'redis://{{ server.broker.host }}:{{ server.broker.port }}/{{ server.broker.number }}'
CELERY_DEFAULT_QUEUE = "{{ app_name }}"
{%- elif  server.broker is defined and server.broker.engine == 'amqp' %}
BROKER_URL = 'amqp://{{ server.broker.user }}:{{ server.broker.password }}@{{ server.broker.host }}:{{ server.broker.get("port",5672) }}/{{ server.broker.virtual_host }}'
{%- endif %}

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

{%- if server.mail.get('encryption', 'none') == 'tls' %}
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
{%- endif %}
{%- if server.mail.get('encryption', 'none') == 'ssl' %}
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
{%- endif %}
EMAIL_HOST = "{{ server.mail.get('host', 'localhost') }}"
EMAIL_HOST_USER = "{{ server.mail.user }}"
EMAIL_HOST_PASSWORD = "{{ server.mail.password }}"
EMAIL_PORT = {{ server.mail.get('port', '25') }}


# http://twitter.com/apps/new
# It's important that input a callback URL, even if its useless. We have no idea why, consult Twitter.
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

# http://developers.facebook.com/setup/
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''

# http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
GOOGLE_OAUTH2_CLIENT_ID = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''

# https://github.com/settings/applications/new
GITHUB_APP_ID = ''
GITHUB_API_SECRET = ''

# https://trello.com/1/appKey/generate
TRELLO_API_KEY = ''
TRELLO_API_SECRET = ''
