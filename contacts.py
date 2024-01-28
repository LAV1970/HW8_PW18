from mongoengine import Document, StringField, BooleanField, EmailField


class Contact(Document):
    full_name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    phone_number = StringField(max_length=20)
    message_sent = BooleanField(default=False)
    preferred_contact_method = StringField(choices=["email", "sms"], default="email")


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
