from django.urls import path
from . import views

# app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('debug_cloudinary/', views.debug_cloudinary, name='debug_cloudinary'),
    path('<str:slug>', views.blog_detail, name='blog_detail'),
    path('category/<str:slug>', views.category, name='category'),
    path('<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('search/', views.search_view, name='search'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
