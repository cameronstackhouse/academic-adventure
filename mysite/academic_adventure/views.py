from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #Used to reject user entry to web page if not logged in
from .models import Event
from .forms import CreateForm
import string 
import random


from .models import Event

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
    gamekeeper = request.user.gamekeeper
    context = {"gamekeeper": gamekeeper}
    return render(request, 'academic_adventure/leaderboard.html', context)

@login_required
def map(request):
    gamekeeper = request.user.gamekeeper
    context = {"gamekeeper": gamekeeper,
                "events":Event.objects.all()}
    return render(request, 'academic_adventure/map.html', context)

@login_required
def scan(request):
    gamekeeper = request.user.gamekeeper
    context = {"gamekeeper": gamekeeper}
    return render(request, 'academic_adventure/scan.html', context)

@login_required
def create(request):
    """Create view. This view allows for a gamekeeper to create
    an activity and generate a QR code for the activity. Create
    also keeps a list of previously generated event QR codes.
    """
    gamekeeper = request.user.gamekeeper
    if request.method == "POST":
        createform = CreateForm(request.POST)
        if createform.is_valid():
            newevent = createform.save()
            # Set host as current and code as a randomly generated code
            newevent.host = request.user
            newevent.code = ''.join(random.choice(string.ascii_uppercase + string.digits) for char in range(6))
            newevent.save()
    else:
        createform = CreateForm(initial={'host':request.user})
    context = {'user': request.user,
               'createform': createform,
               'allevents': Event.objects.filter(host=request.user),
               'gamekeeper': gamekeeper}
    return render(request, 'academic_adventure/create.html', context)

@login_required
def code(request, **kwargs):
    """"""
    gamekeeper = request.user.gamekeeper
    event = Event.objects.get(pk=kwargs['event_id'])
    return render(request, 'academic_adventure/code.html', {"event":event, "gamekeeper":gamekeeper})
