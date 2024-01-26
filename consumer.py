import pika


# Callback-функция для обработки сообщений
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создание очереди с именем 'email_queue'
channel.queue_declare(queue="email_queue")

# Указываем, что используем функцию callback для обработки сообщений
channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
