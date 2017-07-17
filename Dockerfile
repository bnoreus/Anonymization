FROM python:2.7

RUN mkdir -p /my_app/
RUN mkdir -p /my_app/data
RUN mkdir -p /my_app/models
COPY * /my_app/
COPY data/* /my_app/data/
COPY models/* /my_app/models/

RUN pip install -r /my_app/requirements.txt
EXPOSE 80

WORKDIR /my_app
CMD python microservice.py
