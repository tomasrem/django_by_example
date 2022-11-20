# the name of this file is important
from atexit import register
from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

# name of the file is important ==>  eg app_tags.py
register = template.Library() # varaible that needs to be in every _tags.py module to make it work
# also in template you need to specify {% load blog_tags %}

# there are two types of tags ==> simple_tag -> returns a string and inclusion_tag -> procesess given data and returns a template 

@register.simple_tag(name="my_tag") # you can specify the name or you dont have to (the function name would be used)
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html") # you have to specify a template for the tag 
def show_latest_posts(count = 5): # we can pass the count value when we invoke the inclusion_tag
    latest_posts = Post.published.order_by("-publish")[:count]
    return { "latest_posts" : latest_posts } # dictionary is used in template and {% show_latest_posts %} is to invoke the template in your main templater
# inclusion tags have to return a dictionary of values into some template and we can include the template somewhere else


@register.simple_tag
def get_most_commented_posts(count = 5):
    return Post.published.annotate(total_comments = Count("comments")).order_by("-total_comments")[:count]


@register.filter(name="markdown") # we named it to prevent a conflict in names with markdown module :) , we register template tag filters this way btw :)
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

