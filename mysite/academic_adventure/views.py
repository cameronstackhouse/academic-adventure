from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #Used to reject user entry to web page if not logged in

@login_required
def home(request):
    """Homepage view"""

    #Gets user attributes to pass into home.html file
    username = request.user.username
    intelligence = request.user.intelligence
    sociability = request.user.sociability
    athleticism = request.user.athleticism
    score = request.user.score
    gamekeeper = request.user.gamekeeper
    context = {"username":username,
               "intelligence": intelligence,
               "sociability":sociability,
               "athleticism":athleticism,
               "score":score,
               "gamekeeper":gamekeeper}
    return render(request, 'academic_adventure/home.html', context)

@login_required
def leaderboard(request):
    return render(request, 'academic_adventure/leaderboard.html')

@login_required
def map(request):
    return render(request, 'academic_adventure/map.html')

@login_required
def scan(request):
    return render(request, 'academic_adventure/scan.html')