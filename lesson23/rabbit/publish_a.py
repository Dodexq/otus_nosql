#!/usr/bin/env python
import pika, sys

credentials = pika.PlainCredentials('test', 'Passwd321$')
connection = pika.BlockingConnection(pika.ConnectionParameters(sys.argv[1], 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[2:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()