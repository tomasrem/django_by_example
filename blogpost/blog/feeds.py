    #https://docs.djangoproject.com/en/4.1/ref/contrib/syndication/ 


import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatesPostFeed(Feed):
    title = "My blog"
    link = reverse_lazy("blog:post_list")
    description = "New posts of my blog."

    def items(self):
        return Post.published.all()[:5]  # this returns the items 

    def items_title(self,item): # for each item specify title 
        return item.title

    def item_description(self,item): # description 
        return truncatewords_html(markdown.markdown(item.body),30)

    def item_pubdate(self,item): # published date
        return item.publish

    # it gets the item link from get absolute url model method 
    ## otherwwise we have to specify it in item_link(self,item):
    