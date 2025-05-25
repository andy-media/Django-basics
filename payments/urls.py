from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_view, name='payment'),
    path('verify/', views.payment_verify_view, name='payment_verify'),
]