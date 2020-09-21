from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector
# from projects
from .models import Post
from .forms import CommentForm, SearchForm
# thrid party apps
from taggit.models import Tag


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    selected_tag = None
    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=selected_tag)

    return render(request, 'blog/post/list.html', {'posts': posts, 'selected_tag': selected_tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    # listing active comments
    comments = post.comments.filter(active=True) # comments is related_name of comment model
    new_comment = None
    if request.method == 'POST':
        # a comment form was posted
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post =  post
            new_comment.save()
    else:
        # GET request
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body')).filter(search=query)
    
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})
