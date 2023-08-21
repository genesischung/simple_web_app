import pika
import os
import psycopg2

print("Connecting to AMQP server ...")

try:
    url = pika.connection.URLParameters(os.environ.get("CLOUDAMQP_URL"))
    connection = pika.BlockingConnection(url)
except pika.exceptions.AMQPConnectionError as err:
    print("Failed to connect to a AMQP server")
    exit(1)

channel = connection.channel()
channel.queue_declare(queue='message_queue', durable=True)

print("Waiting for messages ...")

try:
    database_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(database_url)
except:
    print("Unable to connect to database")
    print("URL: ".format(database_url))
    exit(1)


def callback(ch, method, properties, body):
    print(" Received: %s" % body.decode())
    with conn.cursor() as curs:
        curs.execute(body)
        conn.commit()
    print("Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='message_queue', on_message_callback=callback)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Exiting message broker ...")
    channel.stop_consuming()
conn.close()
connection.close()



