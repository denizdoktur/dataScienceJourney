from typing import List

from pydantic import BaseModel


class ChapterOutline(BaseModel):
    title: str
    description: str


class ArticleOutline(BaseModel):
    chapters: List[ChapterOutline]


class Chapter(BaseModel):
    title: str
    content: str
