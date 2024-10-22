from django.urls import path
from . import views

urlpatterns = [
    path('', views.scan_site, name='scan_site'),
    path('about/', views.about_page, name='about_page'),

]
