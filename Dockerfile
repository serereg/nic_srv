FROM python:3.7-alpine

WORKDIR /pargolovo_server
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ .
RUN pip install -e .
EXPOSE 8080
CMD ["python", "-m", "pargolovo_server"]
