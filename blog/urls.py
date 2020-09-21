from django.urls import path
# from project
from .import views

'''
 * If using `path()` and converters isn't sufficient for you, you can use `re_path()` instead to define complex URL patterns with Python regular expressions.
'''

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('search/', views.post_search, name='post_search'),
    path('<slug:tag_slug>/', views.post_list, name='list_post_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]