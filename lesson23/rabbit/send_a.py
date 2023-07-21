#!/usr/bin/env python
import pika, sys

credentials = pika.PlainCredentials('test', 'Passwd321$')
connection = pika.BlockingConnection(pika.ConnectionParameters(sys.argv[1], 5672, '/', credentials))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()
