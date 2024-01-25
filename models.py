from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    DateTimeField,
    connect,
)

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
        author = Author(**author_data)
        author.save()

except Exception as e:
    print(f"Error creating author: {e}")

try:
    # Создаем цитаты из JSON
    quotes_data = [
        {
            "tags": ["change", "deep-thoughts", "thinking", "world"],
            "author": "Albert Einstein",
            "quote": "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.",
        },
        {
            "tags": ["inspirational", "life", "live", "miracle", "miracles"],
            "author": "Albert Einstein",
            "quote": "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.",
        },
        {
            "tags": ["adulthood", "success", "value"],
            "author": "Albert Einstein",
            "quote": "Try not to become a man of success. Rather become a man of value.",
        },
        {
            "tags": ["humor", "obvious", "simile"],
            "author": "Steve Martin",
            "quote": "A day without sunshine is like, you know, night.",
        },
    ]

    for quote_data in quotes_data:
        # Find the corresponding author
        author = Author.objects.get(fullname=quote_data["author"])

        # Create a Quote instance
        quote = Quote(
            content=quote_data["quote"],
            author=author,
            tags=quote_data["tags"],
            quote=quote_data["quote"],
        )
        quote.save()

except Exception as e:
    print(f"Error creating quote: {e}")
