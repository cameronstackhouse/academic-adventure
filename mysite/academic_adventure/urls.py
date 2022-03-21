from django.urls import path

from . import views

app_name = 'academic_adventure'
urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'), #Home URL to show users their stats
    path('leaderboard/', views.leaderboard, name='leaderboard'), #Leaderboard URL for showing users their stats vs others
    path('events/', views.events, name='events'), #Leaderboard URL for showing users their stats vs others
    path('create/', views.create, name='create'), #Create URL for creating a new event
    path('create/<str:event_id>/', views.code, name='code'), #URL for a specific event, shows the code for a given event
    path('battle/', views.battle, name='battle'), #URL for the battle, reached by scanning an event. Passes in an event id
    path('leave/<str:code>', views.leave, name='leave'), #URL for leaving an event
    path('buy/<str:path>/<str:url>', views.buy_picture, name='buy') #URL for buying a profile picture
]