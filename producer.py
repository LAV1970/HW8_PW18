import pika
from contacts import Contact

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создание очереди с именем 'email_queue'
channel.queue_declare(queue="email_queue")

# Генерация сообщений и отправка их в очередь
try:
    # Создаем контакты
    contacts_data = [
        {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "message_sent": False,
        },
        {
            "full_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "message_sent": False,
        },
        # Добавьте другие контакты по мере необходимости
    ]

    for contact_data in contacts_data:
        # Создаем контакт
        contact = Contact(**contact_data)
        contact.save()

        # Отправка сообщения в очередь с ObjectID контакта
        message = str(contact.id)
        channel.basic_publish(exchange="", routing_key="email_queue", body=message)

        print(f" [x] Sent '{message}'")

except Exception as e:
    print(f"Error creating contacts and sending messages: {e}")

# Закрытие соединения
connection.close()
