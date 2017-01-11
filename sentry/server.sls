{%- from "sentry/map.jinja" import server with context %}

{%- if server.enabled %}

include:
- python

sentry_packages:
  pkg.installed:
  - names: {{ server.pkgs }}
  - require:
    - pkg: python_packages

/srv/sentry:
  virtualenv.manage:
  - system_site_packages: True
  - requirements: salt://sentry/conf/requirements.txt
  - require:
    - pkg: sentry_packages

sentry_user:
  user.present:
  - name: sentry
  - system: True
  - home: /srv/sentry
  - require:
    - virtualenv: /srv/sentry

sentry_writable_dirs:
  file.directory:
  - mode: 755
  - user: sentry
  - makedirs: True
  - names:
    - /srv/sentry
    - /srv/sentry/logs
    - /srv/sentry/run

sentry_init:
  cmd.run:
  - name: /srv/sentry/bin/sentry init /etc/sentry
  - creates: /etc/sentry
  - require:
    - virtualenv: /srv/sentry

/etc/sentry/sentry.conf.py:
  file:
  - managed
  - source: salt://sentry/conf/sentry.conf.py
  - mode: 644
  - template: jinja
  - require:
    - cmd: sentry_init

sentry_initdb:
  cmd.run:
  - name: SENTRY_CONF=/etc/sentry /srv/sentry/bin/sentry upgrade
  - require:
    - file: /etc/sentry/sentry.conf.py

{%- endif %}