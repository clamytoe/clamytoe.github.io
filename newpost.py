#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import pyperclip

AUTHOR = "Martin Uribe"
ARTICLE_LOCATION = Path("content", "articles")


@dataclass
class Article:
    title: str
    category: str
    tags: List[str]
    summary: str
    markdown: bool

    def __post_init__(self):
        self.category = self.category.title()
        self.date = datetime.today().strftime("%Y-%m-%d %H:%M")
        self.slug = self.title.lower().replace(" ", "-")
        self.author = AUTHOR
        if self.markdown:
            self.location = ARTICLE_LOCATION.joinpath(f"{self.slug}.md")
        else:
            self.location = ARTICLE_LOCATION.joinpath(f"{self.slug}.nbdata")

    def create_file(self):
        header = f"title: {self.title}\n"
        header += f"date: {self.date}\n"
        header += f"category: {self.category}\n"
        header += f"tags: {self.tags}\n"
        header += f"slug: {self.slug}\n"
        header += f"author: {self.author}\n"
        header += f"summary: {self.summary}\n"

        if self.markdown:
            header += f"\n# {self.title}\n\n"
        else:
            pyperclip.copy(self.slug)

        self.location.write_text(header)
        print(f"Generated new article: {self.location}")


def get_bool(subject):
    value = input(f"{subject.capitalize():>10} [y]/n? ")
    if not value:
        return True
    return False


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
    markdown = get_bool("markdown")
    post = Article(title, category, tags, summary, markdown)
    post.create_file()


if __name__ == "__main__":
    main()
