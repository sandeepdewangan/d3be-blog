from django import template
# from project
from ..models import Post


register = template.Library()

'''
    @register.simple_tag(name='my_tag') OR default is function name as tag name.
    Before using tags you must load it.
    {% load blog_tags %}
'''
@register.simple_tag
def total_posts():
    return Post.published.count()