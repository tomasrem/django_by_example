import imp
from django.views.generic import ListView
from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from blogpost.settings import EMAIL_HOST_USER as my_email
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count # allows to perform aggregated counts of tags

from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity


#from django.http import Http404

# Create your views here.

def post_list(request,tag_slug = None):
    #posts = Post.published.all()
    post_list = Post.published.all()  # list of options 
    form = SearchForm()
    # tagging 
    tag = None 
    if tag_slug: # ak je slug passnuty 
        tag = get_object_or_404(Tag, slug=tag_slug) # ziska sa konkretny tag object
        post_list = post_list.filter(tags__in = [tag]) # ziskanie postov ktore obsahuju aj tento tag (post ma viacero tagov) , mozem zadat napr tags_in = ["hudba" , "nieco"] a vrati to zoznam vsetkych kt maju jeden z tagov 

    #Pagination with 3 posts per page
    paginator = Paginator(post_list , 3) # instantinating a class of paginator , passing in list and models per page 
    page_number = request.GET.get("page" , 1) # retrieving the get page from request idk how it works 
    

     # getting the corresponding objects to the current page
    try: 
        posts = paginator.page(page_number)

    except EmptyPage:
        # If page_number is out of range deliver to last pahe of results 
        posts = paginator.page(paginator.num_pages)

        # If the page_number is not an integer smth like askj than do the following
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request,  "blog/post/list.html",  {"posts": posts})


    return render(request,  "blog/post/list.html",  {"posts": posts , "tag" : tag , "form" : form})


class PostListView(ListView):
    #alternative post list view 

    queryset = Post.objects.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"






def post_detail(request,year,month,day,post):
    print(request)
    # try: 
    #     post = Post.published.get(pk = id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found :( .")

    post = get_object_or_404(
        Post ,
        status = Post.Status.PUBLISHED ,
        slug = post , 
        publish__year = year ,
        publish__month = month , 
        publish__day = day
        ) # if the object doesnt exist return 404 wich means not found or link is not right 
    

    # list of active comments for the post
    comments = post.comments.filter(active= True)
    #form for users to comment 
    form = CommentForm()

    # List of similar posts

    # tags ids from the current post eg ["1" , "4" , "6"]
    post_tags_ids = post.tags.values_list("id" , flat = True) ## values list funguje -> z querysetu dostan tuto hodnotu od vsetkych objektov ==> Post.objects.value_list("id" , "title") ==> vrati list tuples s tymi hodnotami a ked tam flat = True tak iba hodnoty bez tupe(funguje len pri jednej hodnote :)

    # Post objects that share one of the tags listed above(one or more) ==> __in field lookup , exclude is to exclude the item from the query
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id = post.id) # filter posts base on if they share the tag with original post

    # .annotate pripise policko[same_tags] ku kazdemu objektu a jeho hodnota je Count("tags") => opocitanie kolko ma objektov pri "tags" policku 
    # a potom cely tento queryset (vsetkych similar_posts) zoradit zostupne podla poctu tych tags objektov a datumu vydania , [:4] zobrazit prve 4 objekty
    similar_posts = similar_posts.annotate(same_tags = Count("tags")).order_by("-same_tags" , "-publish")[:4] ## aha takze tieto sa zoradia tak ze kt maju len jeden tag a zdielaju ho idu prve

    return render(request , "blog/post/detail.html" , {"post" : post , "comments" : comments , "form" : form , "similar_posts" : similar_posts})





def post_share(request,post_id):
    # retrieve post by id 
    post = get_object_or_404(Post , id = post_id , status = Post.Status.PUBLISHED) # get the post and it has to be published 
    sent = False
    if request.method == "POST" :
        #form was submitted 
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form was validated and its finee
            cd = form.cleaned_data

            ## ***********send emial to ************##
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd[ 'name']}'s comments: {cd[ 'comments' ]}"
            
            send_mail(
                subject, 
                message , 
                my_email,
                [cd[ 'to' ]],
                
            )
            sent = True

            ##*************** okee *********************##
    else:
        form = EmailPostForm()
        
    return render(request, "blog/post/share.html" , {"post" : post , "form" : form , "sent" : sent})
    


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED)
    comment = None

    ##**** coment was published **********
    form = CommentForm(data=request.POST)
    if form.is_valid():
        ##Create a comment object without saving it to the database
        comment = form.save(commit=False)
        #Assign the post to the comment
        comment.post = post
        #save the comment to the database
        comment.save()
    return render(request, "blog/post/comment.html" , {"post" : post , "form": form , "comment" : comment})

 # Okej takze zmysel je takyto :
 # 1. zobraz comment_form.html na detail page kt sa viaze na tento view - form method == url na tento view 
 # 2. ked sa koment prida form sa submitne spusti sa tento view a prepne sa na comment.html a podla toho ci bola spravne zadana tak sa bud zbrazi comment_form s errors alebo sucess mesage a prechodo nas5
 
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            #********    trigram searcher   **********
            results = Post.published.annotate(
                similarity = TrigramSimilarity('title' , query),
            ).filter(similarity__gt = 0.1).order_by('-similarity')



#------------ Postgres search ranking classic searcher and shiit-----------------
            # search_vector = SearchVector("title", weight = 'A') + SearchVector('body' , weight = 'B')#in wich fields of the model in database
            # search_query = SearchQuery(query , config = 'spanish') #search query is class to tranform term into class searchable 

            # results = Post.published\
            #     .annotate(search = search_vector,   rank = SearchRank(search_vector,search_query))\
            #     .filter(rank__gte=0.3).order_by("-rank")
                

    return render(request , "blog/post/search.html" , {'query' :query , 'results' : results , 'searchform' : form })

# we check if the form has been submited by checking if the get method contains the 'query' parameter , in the template it works similar 