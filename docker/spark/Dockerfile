FROM jupyter/all-spark-notebook
RUN python -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN jupyter labextension install jupyterlab-plotly @jupyter-widgets/jupyterlab-manager jupyterlab-dash jupyterlab-chart-editor @jupyterlab/latex
COPY ./jupyter_server_config.py /home/jovyan/.jupyter/jupyter_server_config.py
EXPOSE 8888