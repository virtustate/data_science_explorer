
FROM python:3
RUN apt-get update && apt-get install -y \
  telnet supervisor nano nodejs
ENV PYTHONUNBUFFERED 1
RUN pip install poetry
COPY ./pyproject.toml /pyproject.toml
RUN poetry config virtualenvs.create false && poetry install
EXPOSE 8000
EXPOSE 8088
ENTRYPOINT ["/bin/sh","/web/entrypoint.sh"]