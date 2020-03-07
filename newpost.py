#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

AUTHOR = "Martin Uribe"
ARTICLE_LOCATION = Path("content", "articles")


@dataclass
class Article:
    title: str
    category: str
    tags: List[str]
    summary: str

    def __post_init__(self):
        self.category = self.category.title()
        self.date = datetime.today().strftime("%Y-%m-%d %H:%M")
        self.slug = self.title.lower().replace(" ", "-")
        self.author = AUTHOR
        self.location = ARTICLE_LOCATION.joinpath(f"{self.slug}.md")

    def create_file(self):
        header = f"title: {self.title}\n"
        header += f"date: {self.date}\n"
        header += f"category: {self.category}\n"
        header += f"tags: {self.tags}\n"
        header += f"slug: {self.slug}\n"
        header += f"author: {self.author}\n"
        header += f"summary: {self.summary}\n"
        header += f"\n# {self.title}\n\n"

        self.location.write_text(header)
        print(f"Generated new article: {self.location}")


def get_input(subject):
    value = input(f"{subject:>10}: ")
    if not value:
        print(f"No subject provided!")
        exit

    return value.strip()


def get_tags():
    tags = []
    while True:
        tag = input("       tag: ")
        if tag:
            tags.append(tag.strip().lower())
        else:
            break

    return ", ".join(tags)


def main():
    title = get_input("title")
    category = get_input("category")
    tags = get_tags()
    summary = get_input("summary")
    post = Article(title, category, tags, summary)
    post.create_file()


if __name__ == "__main__":
    main()
