from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #Used to reject user entry to web page if not logged in
from .models import Event, CustomUser #Imports user defined models in the system
from .forms import CreateForm
from django.utils.crypto import get_random_string #Imports a random string generator for code generation
import string 
import random
import logging
import datetime
from django.utils import timezone

from .models import Event
from .functions import get_user_positions, compare_positions, user_occupied

@login_required
def leaderboard(request):
    """
    View displaying leaderboards to show a user their stats against other people
    across campus.

    Keyword arguments:
    request -- HttpRequest object 
    """

    intelligence_position, athleticism_position, sociability_position = get_user_positions(request.user) #Gets users positions in each leaderboard

    context = {"scoreusers":sorted(CustomUser.objects.all(), key=lambda u:u.score, reverse = True)[:10], #Sorts users by overall score
            "intusers":sorted(CustomUser.objects.all(), key=lambda u:u.intelligence, reverse = True)[:5], #Sorts users by intelligence score
            "socusers":sorted(CustomUser.objects.all(), key=lambda u:u.sociability, reverse = True)[:5], #Sorts users by sociability score
            "athusers":sorted(CustomUser.objects.all(), key=lambda u:u.athleticism, reverse = True)[:5], #Sorts users by athleticism score
            "user":request.user,
            "intelligence_position": intelligence_position,
            "athleticism_position": athleticism_position,
            "sociability_position": sociability_position
            } #Data to be passed into the html form
    return render(request, 'academic_adventure/leaderboard.html', context) #Returns the leaderboard html page with the context passed in

@login_required
def home(request):
    """
    View for the map where the user can see their location and
    the location of events placed by gamekeepers

    Keyword arguments:
    request -- HttpRequest object 
    """
   
    intelligence_position, athleticism_position, sociability_position = get_user_positions(request.user) #Gets users positions in each leaderboard

    context = {"events":Event.objects.all(), #Gets all events in the database
                "user":request.user,
                "intelligence_position": intelligence_position,
                "athleticism_position": athleticism_position,
                "sociability_position": sociability_position} #Passes user information and event information into the HTML form
    return render(request, 'academic_adventure/home.html', context) #Returns the home html page with the context passed in

@login_required
def events(request):
    """
    View for the map where the user can see their location and
    the location of events placed by gamekeepers

    Keyword arguments:
    request -- HttpRequest object 
    """

    current_datetime = timezone.now() # offset-awared datetime

    valid_radius = 0.00036 #Maximum distance a user can be away from an event and participate
    intelligence_position, athleticism_position, sociability_position = get_user_positions(request.user) #Gets users positions in each leaderboard

    context = {"user":request.user,
               "intelligence_position": intelligence_position,
               "athleticism_position": athleticism_position,
               "sociability_position": sociability_position,
                "events":Event.objects.all(), #Gets all events in the database
                "current_time": current_datetime}

    # Scanner code:

    if request.method == "POST": #If the user has scanned a QR code
        logging.info(request.POST.get("scancontent")) #Finds the event the QR code is for using stored contents of QR code
        
        #Gets user location from post request
        lat = request.POST.get("userlat")
        lng = request.POST.get("userlng")

        #Checks if user location has successfully been accessed
        if lng == "" or lat == "":
            context["message"] = "Error, can't get your location."
            return render(request, 'academic_adventure/events.html', context) #Shows scan page

        #Converts user location to decimal from string
        lat = Decimal(lat)
        lng = Decimal(lng)
        
        #Checks if the code is a digit and if the event ID being scanned exists
        if Event.objects.filter(code=request.POST.get("scancontent")).exists():
            scanned_event = Event.objects.get(code=request.POST.get("scancontent")) #Gets the scanned event

            #Gets the location for the event
            event_lng = scanned_event.longitude
            event_lat = scanned_event.latitude

            #Gets the distance the user is from the event scanned
            distance = compare_positions(lat, lng, event_lat, event_lng)
        
            #Checks if user is already currently participating in an event 
            # This only allows a user to be at one event at once
            if user_occupied(request.user): 
                context["message"] = "You are already signed up for an event. Try again when your current event finishes." #Displays message to user
            else:    
                if request.user not in scanned_event.members.all(): #Checks if user is not already registered for event
                    #Performs a distance check to check that the user is close enough to participate in the event
                    if distance > valid_radius:
                        context["message"] = "Too far away to participate in event" #Error message
            
                    #Checks if the scanned event is joinable (If the current time is between 10 minutes before the start of the event and 5 minutes after the start of the event)
                    elif not scanned_event.joinable():
                        context["message"] = "Can't join event, must be between 10 minutes before the start of the event and 5 minutes after the start."
        
                    else:
                        #If user isn't already registered for an event then apply bonus for attending in person event
                        if scanned_event.type == "Sports":
                            request.user.athleticism += 1 * round(scanned_event.duration) #If sports event then increase the users athleticism. Scaled by duration of the event
                            context["message"] = f"Successfully added to event: {scanned_event.name}. Athleticism increased!"
                        elif scanned_event.type == "Academic":
                            request.user.intelligence += 1 * round(scanned_event.duration) #If academic event then add 1 to users intelligence. Scaled by duration of the event
                            context["message"] = f"Successfully added to event: {scanned_event.name}. Intelligence increased!"
                        elif scanned_event.type == "Social":
                            request.user.sociability += 1 * round(scanned_event.duration) #If social event then add 1 to users sociability. Scaled by duration of the event
                            context["message"] = f"Successfully added to event: {scanned_event.name}. Sociability increased!"
                        elif scanned_event.type == "Battle":
                            request.session['battle_id'] = request.POST.get("scancontent") #Sets the battle ID session variable to the event ID
                            return redirect('academic_adventure:battle') #If battle then redirect to the battle view
            
                        request.user.save() #Saves changes made to the users stats
                        scanned_event.members.add(request.user) #Adds user to the event
                else: #Else if user is already registered for event
                    context["message"] = f"You are already registered for this event."
        else: #If the event does not exist
            context["message"] = "Error, event does not exist."
    
    # Main page code:

    #Retrieving events that are not expired and have the user as a member
    user_event = None
    for event in Event.objects.all().order_by('-date'):
        event_minutes = float(event.duration * 60) #Converting duration to a supported format
        if (request.user in event.members.all()) and (event.date + datetime.timedelta(minutes=event_minutes) >= current_datetime): #Checks if current time is before the events expiry
            if event.type != "Battle":
                user_event = event
                break

    #Retrieving events that are joinable within the next hour for the user
    potential_events = []
    for event in Event.objects.all().order_by('-date'):
        event_minutes = float(event.duration * 60) #Converting duration to a supported format
        if (event.society == None or request.user in event.society.members.all()) and (event.date >= current_datetime >= event.date - datetime.timedelta(hours=1)): #Checks if the event is joinable within the next hour
            potential_events.append(event)
    
    #Retrieving events that are not expired and have the user as the host
    host_events = []
    for event in Event.objects.all().order_by('-date').filter(host=request.user):
        event_minutes = float(event.duration * 60) #Converting duration to a supported format
        if event.date + datetime.timedelta(minutes=event_minutes) >= current_datetime - datetime.timedelta(minutes=20): #Checks that the current time - 20 minutes is before the event expiry and 
            host_events.append(event)
    
    context["userevent"] = user_event #event user is currently in
    context["potentialevents"] = potential_events #Events the user can join in the next hour
    context["hostevents"] = host_events #Events the gamekeeper has created that have not expired
            
    return render(request, 'academic_adventure/events.html', context) #Returns the events html page with the context passed in

@login_required
def create(request):
    """
    Create view. This view allows for a gamekeeper to create
    an activity and generate a QR code for a user to join an activity. Create
    also keeps a list of previously generated event QR codes.

    Keyword arguments:
    request -- HttpRequest object 
    """
    gamekeeper = request.user.gamekeeper #Gets if the user is a gamekeeper
    intelligence_position, athleticism_position, sociability_position = get_user_positions(request.user) #Gets users positions in each leaderboard

    if request.method == "POST": #If the gamekeeper tries to create a game
        createform = CreateForm(request.POST) #Gets the values from the form
        if createform.is_valid(): #Checks if the values are valid
            newevent = createform.save() #If so create a new event
            # Set host as user and code as a randomly generated code
            newevent.host = request.user
            newevent.code = get_random_string(75, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            newevent.save() #Saves the event to the database
            return redirect("academic_adventure:code", event_id = newevent.code) #Redirects user to the new event QR code page
    else:
        createform = CreateForm() #Creates the event creation form
    context = {'user': request.user,
               "gamekeeper": gamekeeper,
               "createform": createform, #Passes form to be displayed to create an event into the html form
               "allevents": Event.objects.filter(host=request.user), #Only shows events being hosted by user
               "intelligence_position": intelligence_position,
               "athleticism_position": athleticism_position,
               "sociability_position": sociability_position
               } #Data to be passed into the html form
    return render(request, 'academic_adventure/create.html', context) #Renders the create html page with the context passed in

@login_required
def code(request, event_id):
    """View to display a QR code for a game.
    This QR code is used for users joining a game.
    To join the user must scan the QR code for an event. They will then be taken 
    to the relevant page based on the event type or stats bonuses will be applied 
    to their account

    Keyword arguments:
    request -- HttpRequest object 
    event_id -- ID of the event to display the code
    """
    intelligence_position, athleticism_position, sociability_position = get_user_positions(request.user) #Gets users positions in each leaderboard

    event = Event.objects.get(code=event_id) #Gets the event from the ID passed into the function
    event_members = event.members.all() #Gets all members of a given event
    context = { "event":event, #The event itself
                "event_members":event_members, #Members of the event
                "user": request.user,
                "intelligence_position": intelligence_position,
                "athleticism_position": athleticism_position,
                "sociability_position": sociability_position,
                } #Information about event name, participants, and if the user is a gamekeeper to be passed to HTML form

    return render(request, 'academic_adventure/code.html', context) #Renders the code html with the context passed in

@login_required
def battle(request):
    """
    View to run a battle for a given event.
    This will run an automated battle, then
    reward the player points through a post request if they win.
    Uses a session variable to pass in the event id of the battle
    to prevent users from entering in the event ID of a battle 
    in the URL and gaining access to a battle that is too far away.
    """

    #Checks if an event ID has been set for the battle (Set in the scan view)
    if not request.session.has_key('battle_id'):
        return redirect("academic_adventure:events") #If not set then the user is redirected to the scan view

    event_id = (request.session['battle_id']) #Gets the event id of the battle
    
    #POST request handling for end of game
    if request.method == "POST":
        if request.POST.get("resultcontent").isdigit():
            if int(request.POST.get("resultcontent")) == 1: #If the player won update their attributes
                request.user.intelligence += 1
                request.user.sociability += 1
                request.user.athleticism += 1
                request.user.save()
            
            return redirect('academic_adventure:home') #redirect after a battle back to home page
    
    #Checks that the event ID passed into the function has an event associated with it
    if not Event.objects.filter(code=event_id).exists():
        return redirect("academic_adventure:events")
        
    current_event = Event.objects.get(code=event_id) #Gets the event being participated in

    #checks the user has not already played this battle (preventing refresh cheating)
    #Also checks to see if the event associated with the ID entered is a battle or not
    if request.user in current_event.members.all() or current_event.type != "Battle":
        return redirect("academic_adventure:events")
        
    current_event.members.add(request.user)
    
    intelligence_position, athleticism_position, sociability_position = get_user_positions(request.user) #Gets users positions in each leaderboard
    
    #Get random opponent excluding the current user
    opponents = list(CustomUser.objects.all().exclude(username=request.user.username))
    opponent = random.choice(opponents)
    
    #Error trapping for cases of 0 stats
    if opponent.athleticism == 0:
        opponent.athleticism += 1
        
    if opponent.sociability == 0:
        opponent.sociability += 1
        
    if opponent.intelligence == 0:
        opponent.intelligence += 1
    
    #Scaling opponent stats to user for fairer battle
    user_total = request.user.athleticism + request.user.sociability + request.user.intelligence
    opponent_total = opponent.athleticism + opponent.sociability + opponent.intelligence
    factor = user_total/opponent_total #Finding by what factor to increase/decrease the opponents stats by
    opponent.athleticism = int(factor*opponent.athleticism)
    opponent.intelligence = int(factor*opponent.intelligence)
    opponent.sociability = int(factor*opponent.sociability)
    
    context = { "user": request.user,
                "opponent": opponent,
                "intelligence_position": intelligence_position,
                "athleticism_position": athleticism_position,
                "sociability_position": sociability_position
                } #Information about the user and their opponent
    return render(request, 'academic_adventure/battle.html', context)

@login_required
def leave(request, code):
    """
    View to remove a user from an event that they are currently
    participating in. This forfeits the users rewards.

    Keyword arguments:
    request -- HttpRequest object 
    """

    if Event.objects.filter(code=code).exists(): #Checks if event with the given code exists
        event = Event.objects.get(code=code) #Gets the event with the code
        #Gets the event attributes
        event_date = event.date 
        event_duration = event.duration
        event_type = event.type
        if request.user in event.members.all(): #Checks if user is in the members of the events 
            current_time = timezone.now() #Gets the current time
            #Checks if event hasn't ended
            if event_date + datetime.timedelta(minutes=float(60 * event_duration)) >= current_time:
                #Checks what type of event the event the user wants to leave is
                if event_type == "Academic":
                    request.user.intelligence = request.user.intelligence - round(event_duration) #Reverts intelligence bonus
                elif event_type == "Social":
                    request.user.sociability = request.user.sociability - round(event_duration) #Reverts sociability bonus
                elif event_type == "Sports":
                    request.user.athleticism = request.user.athleticism - round(event_duration) #Reverts athleticism bonus
                
                event.members.remove(request.user) #Removes the user from the event

                event.save() #Saves the event changes
                request.user.save() #Saves the user changes

    
    return redirect("academic_adventure:events") #Redirects back to the events page
