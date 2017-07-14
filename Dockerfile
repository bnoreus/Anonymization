FROM python:2.7

ADD * /my_app/
RUN pip install -r /my_app/requirements.txt
EXPOSE 80

WORKDIR /my_app
CMD ls
CMD ls data
CMD python microservice.py
