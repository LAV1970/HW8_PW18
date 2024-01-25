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
file_path = "authors.json"  # Updated file path
try:
    with open(file_path, "r", encoding="utf-8") as file:
        authors_data = json.load(file)

    for author_data in authors_data:
        author = Author(**author_data)
        author.save()

except Exception as e:
    print(f"Error loading authors: {e}")
