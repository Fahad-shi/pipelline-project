FROM apache/airflow:2.5.3


COPY requirements.txt /requirements.txt


RUN python -m pip install --upgrade pip


RUN pip install --no-cache-dir --user -r /requirements.txt



