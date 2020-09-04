#!/bin/sh
cp /conf/supervisor/jupyter.conf /etc/supervisor/conf.d/jupyter.conf
mkdir /var/log/jupyterlab/
jupyter notebook --generate-config
cat /root/.jupyter/jupyter_notebook_config.py /conf/jupyterlab.conf.append > /root/.jupyter/jupyter_notebook_config.py
/etc/init.d/supervisor start
cd web
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 --settings=base.settings.docker