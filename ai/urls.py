# interview/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_interview, name='start'),
    path('interview/<int:session_id>/', views.interview_page, name='interview'),
    path('submit/<int:session_id>/', views.submit_answers, name='submit'),
    path('report/<int:session_id>/', views.view_report, name='report'),
]
