FROM jupyter/all-spark-notebook
RUN python -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN python -m mitoinstaller install
EXPOSE 8888