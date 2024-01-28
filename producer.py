import pika
from contacts import Contact

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создание очередей с именами 'email_queue' и 'sms_queue'
channel.queue_declare(queue="email_queue")
channel.queue_declare(queue="sms_queue")

# Генерация контактов и отправка их в соответствующие очереди
try:
    contacts_data = [
        {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone_number": "+123456789",
            "preferred_contact_method": "email",
            "message_sent": False,
        },
        {
            "full_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone_number": "+987654321",
            "preferred_contact_method": "sms",
            "message_sent": False,
        },
        # Добавьте другие контакты по мере необходимости
    ]

    for contact_data in contacts_data:
        contact = Contact(**contact_data)
        contact.save()

        message = str(contact.id)

        # Отправка сообщения в соответствующую очередь в зависимости от предпочтительного метода связи
        if contact.preferred_contact_method == "email":
            channel.basic_publish(exchange="", routing_key="email_queue", body=message)
        elif contact.preferred_contact_method == "sms":
            channel.basic_publish(exchange="", routing_key="sms_queue", body=message)

        print(f" [x] Sent '{message}' to {contact.preferred_contact_method}")

except Exception as e:
    print(f"Error creating contacts and sending messages: {e}")

# Закрытие соединения
connection.close()
