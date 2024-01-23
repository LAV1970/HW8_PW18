from mongoengine import Document, StringField, ReferenceField, connect

# Подключение к MongoDB
password = "2g7aV0LR9IzD2lSD"
connect(f"mongodb+srv://lomakindec1970:{password}@hw8pw18.dxhfdeb.mongodb.net/")


class Author(Document):
    name = StringField(
        required=True, max_length=100, unique=True
    )  # Добавлен параметр unique


class Quote(Document):
    content = StringField(required=True)
    author = ReferenceField(Author, reverse_delete_rule=2)


# Пример использования:
try:
    # Попытка создания автора с уникальным именем
    author = Author.objects.get_or_create(name="John Doe")[0]
except Exception as e:
    print(f"Error creating author: {e}")

try:
    # Создаем цитату, используя ссылку на автора
    quote = Quote(content="Example quote", author=author)
    quote.save()
except Exception as e:
    print(f"Error creating quote: {e}")
