#!/bin/bash
docker system prune
docker build --tag parg:1.0 .
docker run --publish 80:80 -v /home/ssm/Pargolovo/server_test/nic_srv/db:/nic_srv/db --name cont_parg parg:1.0
#./venv/bin/python main.py
#docker  exec -it <container name> /bin/bash
