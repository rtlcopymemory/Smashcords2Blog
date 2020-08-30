import os

hugo_post_frontmatter: str = """+++
title = "{}"
chapter = false
+++
"""

owner_id: int = int(os.getenv("OWNER_ID"))
hugo_root: str = "../hugo-src/{}/"
blog_path: str = "../hugo-src/{}/content/"
