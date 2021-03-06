from django import template
from django.utils.safestring import mark_safe
# from project
from ..models import Post
# third party
import markdown


register = template.Library()

'''
    @register.simple_tag(name='my_tag') OR default is function name as tag name.
    Before using tags you must load it.
    {% load blog_tags %}
'''
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))