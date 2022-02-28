from django.urls import path

from . import views

app_name = 'register'
urlpatterns = [
    path('', views.register, name='register'), #URL to register for the app
    path('privacy-policy/', views.privacy, name='privacy'), #URL for the privacy policy
]