# -*- coding: utf-8 -*-

import tinkerer
import tinkerer.paths

# **************************************************************
# TODO: Edit the lines below
# **************************************************************

# Change this to the name of your blog
project = 'Lime Bean'

# Change this to the tagline of your blog
tagline = 'Blog on software development and infrastructure operation'

# Change this to the description of your blog
description = 'This is lime bean blog that blogs software develpment and infrastructure operations, see more on https://blog.limebean.net'

# Change this to your name
author = 'Jimmy Shen'

# Change this to your copyright string
copyright = '2014, ' + author

# Change this to your blog root URL (required for RSS feed)
website = 'https://blog.limebean.net/'

# **************************************************************
# More tweaks you can do
# **************************************************************

# Add your Disqus shortname to enable comments powered by Disqus
disqus_shortname = 'limebeanbloghttps'

# Change your favicon (new favicon goes in _static directory)
html_favicon = 'limebean.ico'

# Pick another Tinkerer theme or use your own
html_theme = "flat_new"

# Theme-specific options, see docs
html_theme_options = { }

# Link to RSS service like FeedBurner if any, otherwise feed is
# linked directly
rss_service = None

# Generate full posts for RSS feed even when using "read more"
rss_generate_full_posts = False

# Number of blog posts per page
posts_per_page = 10

# Character use to replace non-alphanumeric characters in slug
slug_word_separator = '_'

# **************************************************************
# Edit lines below to further customize Sphinx build
# **************************************************************

# Add other Sphinx extensions here
extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus']

# Add other template paths here
templates_path = ['_templates']

# Add other static paths here
html_static_path = ['_static', tinkerer.paths.static]

# Add other theme paths here
html_theme_path = ['_themes', tinkerer.paths.themes]

# Add file patterns to exclude from build
exclude_patterns = ["drafts/*", "_templates/*"]

# Add templates to be rendered in sidebar here
html_sidebars = {
    "**": ["recent.html", "searchbox.html"]
}

# **************************************************************
# Do not modify below lines as the values are required by
# Tinkerer to play nice with Sphinx
# **************************************************************

source_suffix = tinkerer.source_suffix
master_doc = tinkerer.master_doc
version = tinkerer.__version__
release = tinkerer.__version__
html_title = project
html_use_index = False
html_show_sourcelink = False
html_add_permalinks = None
