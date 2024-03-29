from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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


def image_detail(request , id , slug ):
    image = get_object_or_404(Image , id = id , slug = slug)
    
    return render(request, 'images/image/detail.html' , {'section' :'images' , 'image' : image})

#image liking 
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id = image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            
            return JsonResponse({'status' : 'ok'})

        except Image.DoesNotExist:
            pass

    return JsonResponse({'status' : 'error'})

