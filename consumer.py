import pika
from contacts import Contact

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создание очереди с именем 'email_queue'
channel.queue_declare(queue="email_queue")


def send_email(contact_id):
    # Здесь можете добавить код для имитации отправки электронного сообщения
    print(f"Sending email to contact with ID: {contact_id}")

    # Обновление статуса message_sent в контакте
    contact = Contact.objects.get(id=contact_id)
    contact.message_sent = True
    contact.save()


def callback(ch, method, properties, body):
    # Получение ObjectID из сообщения
    contact_id = body.decode("utf-8")

    # Имитация отправки электронного сообщения
    send_email(contact_id)

    print(f" [x] Received '{body}'")


# Установка функции обратного вызова для обработки сообщений из очереди
channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages. To exit press Ctrl+C")
channel.start_consuming()
