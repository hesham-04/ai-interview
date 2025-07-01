from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_interview, name='start'),
    path('interview/<int:session_id>/', views.interview, name='interview'),
    path('submit/<int:session_id>/', views.submit, name='submit'),
    path('report/<int:session_id>/', views.report, name='report'),
]
