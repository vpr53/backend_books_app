from dataclasses import dataclass
from datetime import date


@dataclass
class Books:
    book_id: int
    google_id: str
    title: str
    description: str
    publication_year: date
    pages_count: int
    cover_url: str
    authors: str
    category: str
