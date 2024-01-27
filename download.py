from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    DateTimeField,
    connect,
)

# Подключение к MongoDB
password = "4j5hUePFV62x1oNV"
database_name = "hw8pw18"

connect(
    db=database_name,
    username="lomakindec1970",
    password=password,
    host="mongodb+srv://hw8pw18.dxhfdeb.mongodb.net/Beispiel.beispiel",  # Updated URI
    alias="default",
)


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


# Пример использования:
try:
    # Создаем авторов из JSON
    authors_data = [
        {
            "name": "albert_einstein",  # Добавим поле name
            "fullname": "Albert Einstein",
            "born_date": "March 14, 1879",
            "born_location": "in Ulm, Germany",
            "description": "In 1879, Albert Einstein was born in Ulm, Germany. He completed his Ph.D. at the University of Zurich by 1909. His 1905 paper explaining the photoelectric effect, the basis of electronics, earned him the Nobel Prize in 1921...",
        },
        {
            "name": "steve_martin",  # Добавим поле name
            "fullname": "Steve Martin",
            "born_date": "August 14, 1945",
            "born_location": "in Waco, Texas, The United States",
            "description": 'Stephen Glenn "Steve" Martin is an American actor, comedian, writer, playwright, producer, musician, and composer. He was raised in Southern California in a Baptist family, where his early influences were working at Disneyland and Knott\'s Berry Farm...',
        },
    ]

    for author_data in authors_data:
        # Check if author already exists
        existing_author = Author.objects(name=author_data["name"]).first()
        if existing_author:
            print(f"Author '{author_data['name']}' already exists. Skipping...")
        else:
            author = Author(**author_data)
            author.save()

except Exception as e:
    print(f"Error creating author: {e}")
