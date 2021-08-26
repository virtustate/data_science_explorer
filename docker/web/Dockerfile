
FROM python:3
RUN apt-get update && apt-get install -y telnet supervisor nano nodejs npm
ENV PYTHONUNBUFFERED 1

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN python -m mitoinstaller install

# poetry takes a long time to process dependencies
# COPY ./pyproject.toml /pyproject.toml
# RUN pip install poetry
# RUN poetry config virtualenvs.create false && poetry install

EXPOSE 8000
EXPOSE 8088
ENTRYPOINT ["/bin/sh","/web/entrypoint.sh"]