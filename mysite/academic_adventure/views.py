from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #Used to reject user entry to web page if not logged in
from .models import Event, CustomUser
from .forms import CreateForm
import string 
import random
import logging

from .models import Event

@login_required
def leaderboard(request):
    """View displaying leaderboards to show a user their stats vs other people
    across campus"""
    context = {"scoreusers":sorted(CustomUser.objects.all(), key=lambda u:u.score, reverse = True)[:10],
            "intusers":sorted(CustomUser.objects.all(), key=lambda u:u.intelligence, reverse = True)[:5],
            "socusers":sorted(CustomUser.objects.all(), key=lambda u:u.sociability, reverse = True)[:5],
            "athusers":sorted(CustomUser.objects.all(), key=lambda u:u.athleticism, reverse = True)[:5],
            "user":request.user
            }
    return render(request, 'academic_adventure/leaderboard.html', context)

@login_required
def home(request):
    """View for the map where the user can see their location and
    the location of events placed by gamekeepers"""
    context = {"events":Event.objects.all(),
                "user":request.user} #Passes user information and event information into the HTML form
    return render(request, 'academic_adventure/home.html', context)

@login_required
def events(request):
    """View for the map where the user can see their location and
    the location of events placed by gamekeepers"""
    context = {"events":Event.objects.all(),
                "user":request.user} #Passes user information and event information into the HTML form
    return render(request, 'academic_adventure/events.html', context)

@login_required
def scan(request):
    """View to scan a QR code to join an event"""
    context = {"user":request.user}
    if request.method == "POST": #If the user has scanned a QR code
        logging.info(request.POST.get("scancontent")) 
        #Finds the event the QR code is for using stored contents of QR code
        
        #Checks if the code is a digit and if the event ID being scanned exists
        if request.POST.get("scancontent").isdigit() and Event.objects.filter(pk=request.POST.get("scancontent")).exists():
            scanned_event = Event.objects.get(pk=request.POST.get("scancontent")) #Gets the scanned event

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
                context["message"] = f"Successfully added to event: {scanned_event.name}."
            else: #Else if user is already registered for event
                context["message"] = "You are already registered for this event."
        else: #If the event does not exist
            context["message"] = "Error, event does not exist."

            
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
            return redirect("academic_adventure:code", event_id = newevent.id) #Redirects user to the new event QR code page
    else:
        createform = CreateForm(initial={'host':request.user}) #Creates the event creation form
        context = {'user': request.user,
               'createform': createform,
               'allevents': Event.objects.filter(host=request.user), #Only shows events being hosted by user
               'gamekeeper': gamekeeper
               } #Data to be passed into the html form
    return render(request, 'academic_adventure/create.html', context)

@login_required
def code(request, **kwargs):
    """View to display a QR code for a game.
    This QR code is used for users joining a game.
    To join the user must scan the QR code for an event. They will then be taken 
    to the relevant page based on the event type or stats bonuses will be applied 
    to their account"""
    event = Event.objects.get(pk=kwargs['event_id']) #Gets the event from the ID passed into the function
    event_members = event.members.all() #Gets all members of a given event
    context = { "event":event, 
                "event_members":event_members,
                "user": request.user
                } #Information about event name, participants, and if the user is a gamekeeper to be passed to HTML form
    return render(request, 'academic_adventure/code.html', context)
