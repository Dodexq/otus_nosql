#!/usr/bin/env python
import pika, sys

credentials = pika.PlainCredentials('test', 'Passwd321$')
connection = pika.BlockingConnection(pika.ConnectionParameters(sys.argv[1], 5672, '/', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[2] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[3:]) or 'Hello World!'
channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()