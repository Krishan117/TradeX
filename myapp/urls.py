from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('menu/', views.menu, name='menu'),
    path('booking/<str:name>', views.booking, name='booking'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact,name='contact'),
    path('register/', views.register,name='register'),
    path('log_in/', views.log_in,name='log_in'),
    path('log_out/', views.log_out,name='log_out'),
]