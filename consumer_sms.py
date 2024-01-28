import pika
from contacts import Contact

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создание очереди с именем 'sms_queue'
channel.queue_declare(queue="sms_queue")


def send_sms(contact_id):
    print(f"Sending SMS to contact with ID: {contact_id}")
    contact = Contact.objects.get(id=contact_id)
    contact.message_sent = True
    contact.save()


def callback(ch, method, properties, body):
    contact_id = body.decode("utf-8")

    # Имитация отправки SMS
    send_sms(contact_id)

    print(f" [x] Received '{body}'")


channel.basic_consume(queue="sms_queue", on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for SMS messages. To exit press Ctrl+C")
channel.start_consuming()
