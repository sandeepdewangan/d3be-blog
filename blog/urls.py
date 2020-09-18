from django.urls import path
# from project
from .import views


app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
]