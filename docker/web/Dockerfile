
FROM python:3
RUN apt-get update && apt-get install -y \
  telnet
ENV PYTHONUNBUFFERED 1
#WORKDIR "/web"
RUN pip install poetry
COPY ./pyproject.toml /pyproject.toml
RUN poetry config virtualenvs.create false && poetry install
#COPY ./manage.py /web/manage.py
# COPY ./ /web
# WORKDIR "/web"
# RUN python manage.py makemigrations
# RUN python manage.py migrate
EXPOSE 8000
EXPOSE 8088
ENTRYPOINT ["/web/entrypoint.sh"]