#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Martin Uribe"
SITENAME = "Ramblings of an autodidact..."
ALT_NAME = "#! " + SITENAME
SITESUBTITLE = "Random programming stuff"
DESCRIPTION = "A blog about programming, *nix, and software development."
SITEURL = ""
FAVICON = "favicon.ico"
FAVICON_TYPE = "image/vnd.microsoft.icon"

# META_IMAGE = SITEURL + "/static/img/og_logo.jpg"
# META_IMAGE_TYPE = "image/jpeg"

PATH = "content"
STATIC_PATHS = 'content/static'

TIMEZONE = "US/Central"

DEFAULT_LANG = "en"
LOCALE = "en_US.UTF-8"

THEME = (
    "/home/mohh/anaconda3/envs/ghpages/lib/python3.8/site-packages/pelican/themes/mg"
)

# Social widget
SOCIAL = (
    ("twitter", "https://twitter.com/clamytoe"),
    ("github", "https://github.com/clamytoe"),
    ("linkedin", "https://www.linkedin.com/in/martin-uribe/"),
)

SHARE = True

FOOTER = (
    "&copy; 2020 Martin Uribe. All rights reserved.<br>"
    "Code snippets in the pages are released under "
    '<a href="http://opensource.org/licenses/MIT" target="_blank">'
    "The MIT License</a>, unless otherwise specified."
)


DEFAULT_PAGINATION = 10

TAG_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
DIRECT_TEMPLATES = ("index", "categories", "archives", "search", "tipue_search")
TIPUE_SEARCH_SAVE_AS = "tipue_search.json"

RELATIVE_URLS = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None
# AUTHOR_FEED_ATOM = None
# AUTHOR_FEED_RSS = None

DELETE_OUTPUT_DIRECTORY = True

TWITTER_USERNAME = "clamytoe"
# DISQUS_SITENAME = "devsbytes"
# SC_PROJECT = '10224955'
# SC_SECURITY = '1f2cc438'
