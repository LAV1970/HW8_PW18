from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    DateTimeField,
    connect,
)
import json
from datetime import datetime

# Подключение к MongoDB
password = "cRLLsF3zdTdGEC5X"
database_name = "hw8pw18"

connect(
    db=database_name,
    username="lomakindec1970",
    password=password,
    host="hw8pw18.dxhfdeb.mongodb.net",
    alias="default",
)


# Определение моделей
class Author(Document):
    name = StringField(required=True, max_length=100, unique=True)
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class Quote(Document):
    content = StringField(required=True)
    author = ReferenceField(Author, reverse_delete_rule=2)
    tags = ListField(StringField())
    quote = StringField()
    created_at = DateTimeField()


# Загрузка данных из JSON-файлов

# Загрузка авторов
with open("authors.json", "r", encoding="utf-8") as file:
    authors_data = json.load(file)

for author_data in authors_data:
    author = Author(**author_data)
    author.save()

# Загрузка цитат
with open("quotes.json", "r", encoding="utf-8") as file:
    quotes_data = json.load(file)

for quote_data in quotes_data:
    # Находим соответствующего автора
    author = Author.objects.get(fullname=quote_data["author"])

    # Создаем экземпляр цитаты
    quote = Quote(
        content=quote_data["quote"],
        author=author,
        tags=quote_data["tags"],
        quote=quote_data["quote"],
        created_at=datetime.now(),
    )
    quote.save()

print("Данные успешно загружены в базу данных.")
