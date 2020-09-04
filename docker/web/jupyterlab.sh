#!/bin/bash
export DJANGO_SETTINGS_MODULE='base.settings.docker'
jupyter nbextension install --sys-prefix --py vega
jupyter lab --allow-root

