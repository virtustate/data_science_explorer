#!/bin/sh
cp /web/conf/supervisor/jupyter.conf /etc/supervisor/conf.d/jupyter.conf
mkdir /var/log/jupyterlab/
jupyter notebook --generate-config
cp /web/conf/jupyter_server_config.py /root/.jupyter/jupyter_server_config.py
/etc/init.d/supervisor start
cd web
python manage.py makemigrations
python manage.py migrate
python manage.py shell_plus --notebook
DJANGO_SUPERUSER_PASSWORD=django python manage.py createsuperuser \
    --no-input \
    --username=admin \
    --email=my_user@domain.com
python manage.py runserver 0.0.0.0:8000 --settings=base.settings.docker