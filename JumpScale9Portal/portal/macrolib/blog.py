import re
from js9 import j


class BlogPost:

    def __init__(self, file_name):
        self.file_name = file_name

        # remove comments & metadata
        self.file_content = open(file_name).read()
        self.content = '\n'.join(l for l in self.file_content.splitlines() if not l.startswith(('#', '@')))

    @staticmethod
    def get_posts_in(base_name):
        blog_files = j.sal.fs.listFilesAndDirsInDir(j.sal.fs.getDirName(base_name), True, filter="*.wiki", type="f")
        blog_posts = [BlogPost(file) for file in blog_files]
        blog_posts = sorted([post for post in blog_posts if post.date and post.title],
                            key=lambda p: p.date,
                            reverse=True)
        return blog_posts

    @property
    def url(self):
        return j.sal.fs.getBaseName(self.file_name).replace(".wiki", "")

    @property
    def date(self):
        try:
            return re.search(r'@date\s+(\d{4}-\d{2}-\d{2})', self.file_content).group(1)
        except AttributeError:
            return None

    @property
    def title(self):
        try:
            return re.search(r'@title\s+(.+)', self.file_content).group(1)
        except AttributeError:
            return self.url
