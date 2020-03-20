#!/home/mohh/anaconda3/envs/ghpages/bin/python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

THEME = "themes/mg"

# Site and name settings
AUTHOR = "Martin Uribe"
SITENAME = "Ramblings"
ALT_NAME = "#! " + SITENAME
SITESUBTITLE = "of an autodidact..."
DESCRIPTION = (
    "A blog about my struggles and learning about programming,"
    " software development and life."
)
SITEURL = ""
FAVICON = "favicon.ico"
FAVICON_TYPE = "image/vnd.microsoft.icon"

# plugins
MARKUP = ("md", "ipynb")
PLUGIN_PATHS = ["./plugins"]
PLUGINS = [
    "ipynb.markup",
    "readtime",
    "render_math",
    "liquid_tags.include_code",
    "liquid_tags.literal",
    "liquid_tags.notebook",
    "liquid_tags.video",
    "liquid_tags.youtube",
]
IGNORE_FILES = [".ipynb_checkpoints"]
IPYNB_USE_METACELL = False
IPYNB_SKIP_CSS = True

# Render math settings
MATH_JAX = {
    "align": "left",
    "linebreak_automatic": True,
    "responsive": True,
    "responsive_break": 1125,
}

# Path settings
PATH = "content"
STATIC_PATHS = ["static"]

# Time and Date settings
TIMEZONE = "US/Central"
DEFAULT_LANG = "en"
LOCALE = "en_US.UTF-8"

FOOTER = (
    "&copy; 2020 Martin Uribe. All rights reserved.<br>"
    "Code snippets in the pages are released under "
    '<a href="http://opensource.org/licenses/MIT" target="_blank">'
    "The MIT License</a>, unless otherwise specified."
)

# URL settings
TAG_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
ARTICLE_URL = "articles/{date:%Y}/{date:%b}/{date:%d}/{slug}"
ARTICLE_SAVE_AS = "articles/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html"
PAGE_URL = "pages/{slug}"
PAGE_SAVE_AS = "pages/{slug}/index.html"
DIRECT_TEMPLATES = ("index", "categories", "archives", "search", "tipue_search")
TIPUE_SEARCH_SAVE_AS = "tipue_search.json"

RELATIVE_URLS = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DELETE_OUTPUT_DIRECTORY = True

# Page settings
TWITTER_USERNAME = "clamytoe"

# Social widget
SOCIAL = (
    ("twitter", "https://twitter.com/clamytoe"),
    ("github", "https://github.com/clamytoe"),
    ("github-alt", "https://gist.github.com/clamytoe"),
    ("linkedin", "https://www.linkedin.com/in/martin-uribe/"),
    ("user", "https://www.blog.pythonlibrary.org/2019/11/18/pydev-of-the-week-martin-uribe/"),
    ("coffee", "https://pybit.es/author/martin-uribe.html"),
    ("drupal", "https://codechalleng.es/profiles/clamytoe"),
)
META_IMAGE = SITEURL + "/img/clamytoe.png"
META_IMAGE_TYPE = "image/png"
SHARE = True

DEFAULT_PAGINATION = 10
