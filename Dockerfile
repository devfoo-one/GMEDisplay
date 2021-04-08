FROM python:3-stretch

COPY * /app/

RUN apt-get update -y && apt install -y tzdata

RUN pip install -r /app/requirements.txt

ENTRYPOINT python3 /app/run.py