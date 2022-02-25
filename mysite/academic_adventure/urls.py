from django.urls import path

from . import views

app_name = 'academic_adventure'
urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('map/', views.map, name='map'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('scan/', views.scan, name='scan'),
    path('create/', views.create, name='create'),
    path('create/<int:event_id>/', views.code, name='code')
]