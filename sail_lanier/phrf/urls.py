from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rules/', views.rules, name='rules'),
    path('documents/', views.downloads, name='documents'),
    path('officers/', views.officers, name='officers'),
    path('contact/', views.contact, name='contact'),
    path('contact/<int:user_id>/', views.contact, name='contact'),
    path('contact_success/', views.contact_success, name='contact_success'),
]
