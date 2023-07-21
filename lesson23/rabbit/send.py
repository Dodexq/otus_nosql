#!/usr/bin/env python
import pika

from sys import argv
print(argv[1])
connection = pika.BlockingConnection(pika.ConnectionParameters(argv[1]))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()
