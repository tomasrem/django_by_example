from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    def items(self):
        return Post.published.all()
    def lastmod(self, obj):
        return obj.updated
#https://docs.djangoproject.com/en/4.1/ref/contrib/sitemaps/
# creating xml files with links and some other atributes(priority etc ) for search engine crawlers , its not complicated
# moc to nechapem viem co to robi ale je to troska komplikovaneho charakteru 