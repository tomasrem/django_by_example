from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

# Create your views here.

@login_required
def image_create(request):
    if request.method == 'POST':
        # form is send 
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            #if the form is valid
            cd = form.cleaned_data
            new_image = form.save(commit = False)
            # assign current user to the image 
            new_image.user = request.user
            new_image.save()
            messages.success(request , 'Image added successfully')

            #redirect to the new created item detail view
            return redirect(new_image.get_absolute_url())

    else:
        # build form with the data provided by the bookmarklet via get , ust get some data from the url 
        form = ImageCreateForm(data=request.GET)

    return render(request , 'images/image/create.html' , {'section' : 'images'  , 'form' : form})