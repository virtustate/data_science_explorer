
FROM python:3
RUN apt-get update && apt-get install -y \
  telnet supervisor nano nodejs npm
ENV PYTHONUNBUFFERED 1
RUN pip install poetry
COPY ./pyproject.toml /pyproject.toml
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN poetry config virtualenvs.create false && poetry install
EXPOSE 8000
EXPOSE 8088
ENTRYPOINT ["/bin/sh","/web/entrypoint.sh"]