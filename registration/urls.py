from django.urls import path
from . import views

urlpatterns = [
    path('school/', views.school_info_view, name='school_info'),
    path('contestants/', views.contestant_info_view, name='contestant_info'),
    path('coaches/', views.coach_info_view, name='coach_info'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('receipt/<int:payment_id>/pdf/', views.generate_receipt_pdf, name='receipt_pdf'),
    path('download-all/', views.download_questions, name='download_all'),

]