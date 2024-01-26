import pika

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создание очереди с именем 'email_queue'
channel.queue_declare(queue="email_queue")

# Отправка сообщения
message = "Hello, this is a test email message!"
channel.basic_publish(exchange="", routing_key="email_queue", body=message)

print(f" [x] Sent '{message}'")

# Закрытие соединения
connection.close()
