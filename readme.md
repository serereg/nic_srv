# IoT SCADA

## The project consist of 

1. Application-Server,

2. IoT-Gateway,

3. Program Logic Controller (PLC).

4. Sensors and valves

PLC and IoT-Gateway are located in a factory. 

PLC controls technological process (i.e. temperature in coolers with beer), 
IoT-Gateway is "proxy" between PLC and Application-Server


## Application-Server 
is analog of web-SCADA. It provides web-interface for operators.


## IoT-Gateway
connets to PLC via ModbusTCP. 
Sends alarms via Telegram.


## PLC

contols the technological process.


### Todos
 - use vue.js
 - make html-template

 - use PostgreSQL and time series for trends

 - use local copy of css bootstrap

 - use database for telegram clients 
 - jinja for telegram messages

 - change modbus library. Use mock

 - refactor IoT-Gateway

 - use json config file for ip, token etc

 - use MQTT, RabbitMQ..
