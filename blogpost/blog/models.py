

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)







class Post(models.Model):
    class Status(models.TextChoices):  # if we inherit from texchoices it  restrict changing the given variables later in code 
        DRAFT = "DF" , "Draft"
        PUBLISHED = "PB" , "Published "



    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250 , unique_for_date = "publish")
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 2, choices = Status.choices , default = Status.DRAFT)
    
    author = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "blog_posts" , null = True )  # related name is user.Post_set

    objects = models.Manager() # this is the default model manager for every model , we have to add it bc if we overwrite the default manager would be published instead of objects, also we can specify the def manager in meta . default_manager_name 
    published = PublishedManager() # this is our custom query manager defined above 

    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"] #ordering by publish date ascending , in meta class we can write meta options to the database 
        indexes = [
            models.Index(fields=["-publish"]),   # indexing is making a B-tree in database 
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self): # moc to nechapem o co tu ide 
        return reverse("blog:post_detail" , args=[self.publish.year , self.publish.month , self.publish.day , self.slug])

    

    ## when we are using .filter() on query we specifiy fields as .filter(publis__year = 2022 , author__username = "tomas")ň


class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete = models.CASCADE , related_name = "comments")
    name = models.CharField(max_length = 80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields = ["created"],)
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}" 

