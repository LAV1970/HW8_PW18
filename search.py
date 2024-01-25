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


def search_quotes_by_tags(tags):
    quotes = Quote.objects(tags__in=tags)
    print("Search Results:")
    for quote in quotes:
        print(f"Author: {quote.author.fullname}, Quote: {quote.content}")
    print("\n")


def search_quotes_by_author(author_name):
    author = Author.objects(name=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        print("Search Results:")
        for quote in quotes:
            print(f"Quote: {quote.content}")
        print("\n")
    else:
        print(f"Author '{author_name}' not found.\n")


def search_quotes_by_tags_and_author(tags, author_name):
    author = Author.objects(name=author_name).first()
    if author:
        quotes = Quote.objects(tags__in=tags, author=author)
        print("Search Results:")
        for quote in quotes:
            print(f"Quote: {quote.content}")
        print("\n")
    else:
        print(f"Author '{author_name}' not found.\n")


def main():
    while True:
        user_input = input("Enter command (tags, author, exit): ")
        if user_input == "exit":
            print("Exiting the program.")
            break
        elif user_input == "tags":
            tags_input = input("Enter tags (comma-separated): ")
            tags = [tag.strip() for tag in tags_input.split(",")]
            search_quotes_by_tags(tags)
        elif user_input == "author":
            author_name = input("Enter author name: ")
            search_quotes_by_author(author_name)
        elif user_input == "both":
            tags_input = input("Enter tags (comma-separated): ")
            tags = [tag.strip() for tag in tags_input.split(",")]
            author_name = input("Enter author name: ")
            search_quotes_by_tags_and_author(tags, author_name)
        else:
            print(
                "Invalid command. Please enter 'tags', 'author', 'both', or 'exit'.\n"
            )


if __name__ == "__main__":
    main()
