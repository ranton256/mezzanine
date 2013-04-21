from datetime import timedelta
from time import timezone
from optparse import make_option
from django.core.management.base import CommandError
from mezzanine.blog.management.base import BaseImporterCommand

class Command(BaseImporterCommand):
    """
    Import a Blogspot feed into the blog app.
    """
    
    option_list = BaseImporterCommand.option_list + (
                                                     make_option("-s", "--url", dest="url",
                                                                 help="Blogspot Atom feed url"),
                                                     )
    
    def handle_import(self, options):
        url = options.get("url")
        if not url:
            raise CommandError("--url option "
                               "must be specified")

        try:
            from dateutil import parser
        except ImportError:
            raise CommandError("dateutil package is required")
        try:
            from feedparser import parse
        except ImportError:
            raise CommandError("feedparser package is required")
                
        posts = parse(url)["entries"]
        for post in posts:
            pub_date = parser.parse(post.updated)
            pub_date -= timedelta(seconds=timezone)
            self.add_post(title=post.title, content=post.content[0]["value"],
                          pub_date=pub_date, 
                          old_url=None)
