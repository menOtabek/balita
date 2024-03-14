from django.urls import path
from .views import home_view, blog_detail_view, category_view, contact_view, about_view, search_view, tag_view

urlpatterns = [
    path('', home_view),
    path('blog/<int:pk>/', blog_detail_view),
    path('category/', category_view),
    path('contact/', contact_view),
    path('about/', about_view),
    path('search/', search_view),
    path('tag/', tag_view)
]