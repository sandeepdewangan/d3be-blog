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


### Adding a sitemap to your site (not implemented)
Django comes with a sitemap framework, which allows you to generate sitemaps for your site dynamically. A sitemap is an XML file that tells search engines the pages of your website, their relevance, and how frequently they are updated.

### Creating feeds for your blog posts (not implemented)
Django has a built-in syndication feed framework that you can use to dynamically generate RSS or Atom feeds in a similar manner to creating sitemaps using the site's framework.
