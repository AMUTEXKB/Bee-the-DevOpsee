# Bee the DevOpsee
Our beloved Bee has an application that consumes from a queue, Bee wants to define and automate how the queue and the application run in development. After asking chatGPT, it responded with Docker-Compose being a good way to do it.


Our goal is to help Bee write her very first docker-compose.yaml file, with 2 services:

rabbitmq with the image rabbitmq:3.9.28-management, the container should be called rabbitmq and it should publish its AMQP port and Managment ports on the same default ports. Also configures rabbitmq with a default username "bee" and password "beebee123".
consumer with its build definition within the file and also waits for the rabbitmq service to be up and also for the port to be accessible in order to start the consumer workload with the tool wait-for-it.sh.
Both should be in the same bridge network called my_network.

# Project Tree
.
├── Dockerfile
├── consumer.py
├── docker-compose.yaml
└── requirements.txt


# How to Run RabbitMQ and Consumer with Docker Compose
This guide will show you how to define and automate how the queue and the application run in development using Docker Compose.

 # Prerequisites
Make sure that you have the following installed on your system:

# Docker
Docker Compose
# Step 1: Project Tree
Make sure that you have the following project tree:
```
.
├── Dockerfile
├── consumer.py
├── docker-compose.yaml
└── requirements.txt
```

# Step 2: Dockerfile
Create a Dockerfile with the following content:
```

FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED="true"
RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /bin/wait-for-it.sh \
      && chmod a+x /bin/wait-for-it.sh
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY consumer.py .
```

This Dockerfile will use the Python 3.10-bullseye image and install the required dependencies for the consumer application. It will also copy the consumer.py file to the container.

# Step 3: consumer.py
Create a consumer.py file with the following content:
```
import pika
from os import environ
 
amqp_url = environ["AMQP_URL"]
 
 
def on_queue_message(ch, method, properties, body):
    print('Got a message from Queue: ', body)
 
 
def main():
    parameters = pika.URLParameters(amqp_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare('test', durable=True, exchange_type='topic')
    channel.basic_consume(
        queue='jobs', on_message_callback=on_queue_message, auto_ack=True)
    print("Starting consumption")
    channel.start_consuming()
 
 
if __name__ == '__main__':
    main()
```
This file contains the code for the consumer application. It uses the Pika library to consume messages from a RabbitMQ queue.

# Step 4: docker-compose.yaml
Create a docker-compose.yaml file with the following content:

```
version: '3.9'
services:
  rabbitmq:
    image: rabbitmq:3.9.28-management
    container_name: rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: bee
      RABBITMQ_DEFAULT_PASS: beebee123
    ports:
      - "5672:5672"
      - "15672:15672"
    networks:
      - my_network

  consumer:
    build: .
    depends_on:
      rabbitmq:
        condition: service_healthy
    command: ["./wait-for-it.sh", "rabbitmq:5672", "--", "python", "consumer.py"]
    networks:
      - my_network

networks:
  my_network:
    driver: bridge
```
This file defines two services: rabbitmq and consumer. RabbitMQ uses the rabbitmq:3.9.28-management image and is configured with a default username and password. It also publishes its AMQP and Management ports on the same default ports.

Consumer is built from the Dockerfile in the same directory and waits for RabbitMQ to be up and the port to be accessible using the wait-for-it.sh tool. Once RabbitMQ is up, it starts the consumer workload. It also defines an environment variable with the AMQP URL.

Both services are in the same bridge network called my_network.
