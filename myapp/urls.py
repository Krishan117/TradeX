from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('menu/', views.menu, name='menu'),
    path('booking/', views.booking, name='booking'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact,name='contact',)
]