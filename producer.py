import pika
from mongoengine import Document, StringField, BooleanField
from contacts import create_contact  # Импортируем модель Contact из contacts.py


class Contact(Document):
    full_name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100, unique=True)
    message_sent = BooleanField(default=False)


# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создание очереди с именем 'email_queue'
channel.queue_declare(queue="email_queue")

# Отправка сообщения
message = "Hello, this is a test email message!"
channel.basic_publish(exchange="", routing_key="email_queue", body=message)

print(f" [x] Sent '{message}'")

create_contact()

# Закрытие соединения
connection.close()
