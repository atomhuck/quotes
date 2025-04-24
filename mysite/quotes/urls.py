from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('faculties', views.facs, name='facs'),
    path('faculties/<slug:slug>/', views.faculty_detail, name='faculty_detail'),
]