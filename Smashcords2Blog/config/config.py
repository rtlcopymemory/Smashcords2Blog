import os
from typing import List

hugo_post_frontmatter: str = """---
title: "{}"
date: 2020-08-08T17:48:37+02:00
slug: "{}"
description: ""
keywords: []
draft: false
tags: []
math: false
toc: false
---
"""

owner_id: int = int(os.getenv("OWNER_ID"))
hugo_root: str = "../hugo-src/"
blog_path: str = "../hugo-src/content/"

config_toml_default: str = """\
theme = "hugo-theme-codex" 

title = "Smashcords Blog"
languageCode = "en-us"
baseURL = "https://smashcordsblog.org/"
copyright = "© {year}"

# disqusShortname = ""
# googleAnalytics = "" 

[params]
  dateFormat = "Jan 2 2006"

[markup]
  [markup.highlight]
    codeFences = false
  [markup.goldmark.renderer]
      unsafe = false

[[menu.main]]
  identifier = "home"
  name = "home"
  title = "Home"
  url = "/"

"""

server_menu_template: str = """\
[[menu.main]]
  identifier = "{0}"
  name = "{0}"
  title = "{1}"
  url = "/{1}"

"""


def create_hugo_config_file(servers: List[tuple]):
    result: str = config_toml_default
    for server in servers:
        result += server_menu_template.format(server[1].lower(), server[1])
    with open(hugo_root + "config.toml", "w+") as f:
        f.write(result)
