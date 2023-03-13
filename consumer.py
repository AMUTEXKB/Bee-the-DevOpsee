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