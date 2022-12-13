from django import forms
from .models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests

# our forms 

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image # form connected to he model 
        fields = ['title' , 'url' , 'description' ] # field that are affected 
        widgets = { # html widgets for the fields
            'url': forms.HiddenInput,
        }


    def clean_url(self):

        url = self.cleaned_data['url']
        valid_extensions = ['jpg' , 'jpeg' , 'png']
        extension = url.rsplit('.' , 1) [1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError('The given url does not match valid image extension! ')

        return url # if its okay return the url value else raise validation error

    def save(self , force_insert = False , force_update = False , commit = True): # editing the save method of the model 

        image = super().save(commit=False) # image is created but not assigned to the database
        image_url = self.cleaned_data['url'] #retrieving the url 
        name = slugify(image.title)   
        extension = image_url.rsplit('.' , 1)[1].lower() ## rsplit is just split but starting from the end of the string
        image_name = f'{name}.{extension}' # image name is created
 
        # download the image from the url 
        response = requests.get(image_url)
        image.image.save(image_name , ContentFile(response.content), save = False) # image model.image field svae method()
        
        if commit: # to maintain the same behavior as the original save() the form is only saved the commit=True
            image.save()
        return image
