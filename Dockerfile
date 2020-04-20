FROM python:3.7-slim

WORKDIR /nic_srv
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ .
EXPOSE 80
CMD ["python", "main.py"]
