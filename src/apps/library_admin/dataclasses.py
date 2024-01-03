from dataclasses import dataclass


@dataclass
class BookDataclass:
    id: int
    title: str
    subtitle: str
    authors: list
    categories: list
    publication_date: str
    editor: str
    description: str
    image: str | None
