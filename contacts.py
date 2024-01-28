from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    full_name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100, unique=True)
    message_sent = BooleanField(default=False)


def create_contact():
    try:
        # Создаем контакт
        contact_data = {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "message_sent": False,
        }

        contact = Contact(**contact_data)
        contact.save()

    except Exception as e:
        print(f"Error creating contact: {e}")
