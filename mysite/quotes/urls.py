from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('faculties', views.facs, name='facs'),
    path('faculties/<slug:slug>/', views.faculty_detail, name='faculty_detail'),
    path('popular', views.popular_quotes, name='popular_quotes'),
    path('about_us', views.about_us, name='about'),
    path('professors/', views.profs, name='profs'),
    path('professors/<slug:slug>/', views.professor_detail, name='professor_detail'),
    path('search/', views.search_professors, name='search_professors'),
    path('search_faculties/', views.search_faculties, name='search_faculties'),
]