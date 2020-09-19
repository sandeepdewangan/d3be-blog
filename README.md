## Blog 

### Query Sets

* Get retrives single object - `User.objects.get(username='admin')`
* Retrives all objects - `Post.objects.all()`
* Savign and deleting objects - `post.delete()` and `post.save()`

### Tagging (django_taggit)

Example:
```python 
>>> from blog.models import Post
>>> post = Post.objects.get(id=1)
>>> post
<Post: Django a powerful web development framework>
>>> post.tags.add('web development', 'python', 'django')
>>> post.tags.all()
<QuerySet [<Tag: web development>, <Tag: django>, <Tag: python>]>
```

### Custom template tags
Django provides the following helper functions that allow you to create your own template tags in an easy manner:
* simple_tag : Processes the data and returns a string
* inclusion_tag : Processes the data and returns a rendered template


