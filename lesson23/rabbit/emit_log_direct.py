#!/usr/bin/env python
import pika, sys

credentials = pika.PlainCredentials('test', 'Passwd321$')
connection = pika.BlockingConnection(pika.ConnectionParameters(sys.argv[1], 5672, '/', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[2] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[3:]) or 'Hello World!'
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()