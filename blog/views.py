from django.shortcuts import render, get_object_or_404
# from projects
from .models import Post
from .forms import CommentForm


def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

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
