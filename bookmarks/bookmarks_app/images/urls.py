from django.urls import path
from . import views

#url patters for the app images
app_name = 'images'
urlpatterns = [
    path('create/' , views.image_create , name='create'),
]