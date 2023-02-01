import pika

connection_parameters = pika.ConnectionParameters('127.0.0.1')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='letterbox')

message = "Hello, world!"

channel.basic_publish(exchange='', routing_key='letterbox', body=message)

print("Sent message.")

connection.close()