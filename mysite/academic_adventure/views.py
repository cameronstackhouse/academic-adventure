from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #Used to reject user entry to web page if not logged in
from .models import Event, CustomUser
from .forms import CreateForm
import string 
import random
import logging


from .models import Event

@login_required
def home(request):
    """Homepage view to show the user their stats"""

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
    return render(request, 'academic_adventure/home.html', context) #Renders home.html template and passes in context

@login_required
def map(request):
    """View for the map where the user can see their location and
    the location of events placed by gamekeepers"""
    gamekeeper = request.user.gamekeeper #Gets if the user is a gamekeeper
    context = {"gamekeeper": gamekeeper,
                "events":Event.objects.all()} #Passes user information and event information into the HTML form
    return render(request, 'academic_adventure/map.html', context)

@login_required
def scan(request):
    """View to scan a QR code to join an event"""
    gamekeeper = request.user.gamekeeper #Gets if the user is a gamekeeper
    context = {"gamekeeper": gamekeeper}
    if request.method == "POST": #If the user has scanned a QR code
        logging.info(request.POST.get("scancontent")) 
        #Finds the event the QR code is for using stored contents of QR code
        scanned_event = Event.objects.get(pk=request.POST.get("scancontent"))

        if request.user not in scanned_event.members.all(): #Checks if user is not already registered for event
            #If user isn't already registered for an event then apply bonus for attending in person event
            if scanned_event.type == "Sports":
                request.user.athleticism += 1 #If sports event then add 1 to the users athleticism
            elif scanned_event.type == "Academic":
                request.user.intelligence += 1 #If academic event then add 1 to users intelligence
            elif scanned_event.type == "Social":
                request.user.sociability += 1 #If social event then add 1 to users sociability
            elif scanned_event.type == "Battle":
                #TODO: Redirect to battle system
                pass
            
            request.user.save() #Saves changes made to the users stats
    
        scanned_event.members.add(request.user) #Adds user to the event
    return render(request, 'academic_adventure/scan.html', context) #Shows scan page

@login_required
def create(request):
    """Create view. This view allows for a gamekeeper to create
    an activity and generate a QR code for a user to join an activity. Create
    also keeps a list of previously generated event QR codes.
    """
    gamekeeper = request.user.gamekeeper
    if request.method == "POST": #If the gamekeeper tries to create a game
        createform = CreateForm(request.POST) #Gets the values from the form
        if createform.is_valid(): #Checks if the values are valid
            newevent = createform.save() #If so create a new event
            # Set host as current and code as a randomly generated code
            newevent.host = request.user
            newevent.code = ''.join(random.choice(string.ascii_uppercase + string.digits) for char in range(6)) #Adds code to event (NOT NEEDED ANYMORE)
            newevent.save() #Saves the event to the database
    else:
        createform = CreateForm(initial={'host':request.user})
    context = {'user': request.user,
               'createform': createform,
               'allevents': Event.objects.filter(host=request.user),
               'gamekeeper': gamekeeper}
    return render(request, 'academic_adventure/create.html', context)

@login_required
def code(request, **kwargs):
    """View to display a QR code for a game.
    This QR code is used for users joining a game.
    To join the user must scan the QR code for an event. They will then be taken 
    to the relevant page based on the event type or stats bonuses will be applied 
    to their account"""
    gamekeeper = request.user.gamekeeper
    event = Event.objects.get(pk=kwargs['event_id']) #Gets the event from the ID passed into the function
    event_members = event.members.all() #Gets all members of a given event
    context = { "event":event, 
                "gamekeeper":gamekeeper, 
                "event_members":event_members
    } #Information about event name, participants, and if the user is a gamekeeper to be passed to HTML form
    return render(request, 'academic_adventure/code.html', context)
