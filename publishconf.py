#!/home/mohh/anaconda3/envs/ghpages/bin/python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys

from pelicanconf import *

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

sys.path.append(os.curdir)

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = "https://clamytoe.github.io"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""
