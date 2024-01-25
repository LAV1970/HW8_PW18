from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    DateTimeField,
    connect,
)
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


def search_quotes_by_name(author_name):
    author = Author.objects(name=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        print("Search Results:")
        for quote in quotes:
            print(f"Quote: {quote.content}")
        print("\n")
    else:
        print(f"Author '{author_name}' not found.\n")


def search_quotes_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    print("Search Results:")
    for quote in quotes:
        print(f"Author: {quote.author.fullname}, Quote: {quote.content}")
    print("\n")


def search_quotes_by_tags(tags):
    quotes = Quote.objects(tags__in=tags)
    print("Search Results:")
    for quote in quotes:
        print(f"Author: {quote.author.fullname}, Quote: {quote.content}")
    print("\n")


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
            search_quotes_by_tag(tag)
        elif user_input.startswith("tags:"):
            tags_input = user_input[5:].strip()
            tags = [tag.strip() for tag in tags_input.split(",")]
            search_quotes_by_tags(tags)
        else:
            print("Invalid command. Please enter a valid command or 'exit'.\n")


if __name__ == "__main__":
    main()
