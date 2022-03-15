from django.urls import path

from . import views

app_name = 'academic_adventure'
urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'), #Home URL to show users their stats
    path('leaderboard/', views.leaderboard, name='leaderboard'), #Leaderboard URL for showing users their stats vs others
    path('events/', views.events, name='events'), #Leaderboard URL for showing users their stats vs others
    path('scan/', views.scan, name='scan'), #Scan URL for scanning a QR code to join or participate in an event
    path('create/', views.create, name='create'), #Create URL for creating a new event
    path('create/<int:event_id>/', views.code, name='code'), #URL for a specific event, shows the code for a given event
    path('battle/<int:event_id>/', views.battle, name='battle') #URL for the battle, reached by scanning an event. Passes in an event id
]