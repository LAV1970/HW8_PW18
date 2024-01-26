from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    DateTimeField,
    connect,
)
from datetime import datetime

from redis import StrictRedis

# Создаем подключение к Redis
redis_client = StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

# Время жизни кеша в секундах (например, 1 час)
CACHE_EXPIRATION_TIME = 3600

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


def search_quotes_by_name(author_name):
    # Проверяем, есть ли результат в кеше
    cached_result = redis_client.get(f"author_search:{author_name}")
    if cached_result:
        print("Search Results (from cache):")
        print(cached_result)
        print("\n")
        return

    author = Author.objects(name__istartswith=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        result = f"Search Results:\n"
        for quote in quotes:
            result += f"Quote: {quote.content}\n"
        print(result)

        # Сохраняем результат в кеш
        redis_client.setex(
            f"author_search:{author_name}", CACHE_EXPIRATION_TIME, result
        )
    else:
        print(f"Author '{author_name}' not found.\n")


def search_quotes_by_tags(tags):
    quotes = Quote.objects(tags__in=tags)
    result = f"Search Results:\n"
    for quote in quotes:
        result += f"Author: {quote.author.fullname}, Quote: {quote.content}\n"
    print(result)

    # Сохраняем результат в кеш
    redis_client.setex(f"tag_search:{tags}", CACHE_EXPIRATION_TIME, result)


def main():
    while True:
        user_input = input(
            "Enter command (name:<author_name>, tag:<tag>, tags:<tag1>,<tag2>, exit): "
        ).strip()
        if user_input.lower() == "exit":
            print("Exiting the program.")
            break
        elif user_input.startswith("name:"):
            author_name = user_input[5:].strip()
            search_quotes_by_name(author_name)
        elif user_input.startswith("tag:"):
            tag = user_input[4:].strip()
            search_quotes_by_tags(tags)
        elif user_input.startswith("tags:"):
            tags_input = user_input[5:].strip()
            tags = [tag.strip() for tag in tags_input.split(",")]
            search_quotes_by_tags(tags)
        else:
            print("Invalid command. Please enter a valid command or 'exit'.\n")


if __name__ == "__main__":
    main()
