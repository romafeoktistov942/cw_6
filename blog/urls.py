from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path("blog/", cache_page(60)(BlogListView.as_view()), name="blog_list"),
    path("blog/<int:pk>/view/", BlogDetailView.as_view(), name="blog_detail"),
]
