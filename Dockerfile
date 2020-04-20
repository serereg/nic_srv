FROM python:3.7-alpine

WORKDIR /nic_srv
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ .
RUN pip install -e .
EXPOSE 80
CMD ["python", "-m", "nic_srv"]