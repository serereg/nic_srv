FROM python:3.7-slim

WORKDIR /nic_srv
COPY ./ .
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["bash", "./entrypoint.sh"]
