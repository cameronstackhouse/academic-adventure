from datetime import timedelta
from math import sqrt
from django.utils import timezone
from .models import CustomUser, Event

def get_user_positions(user):
    """
    Function to get the users positions in the leaderboard rankings. 
    This is used to display the users position to them.

    Keyword arguments:
    user -- user to find leaderboard positions of

    Return:
    Users position in each leaderboard
    """

    #Sorts the data of users by intelligence, athleticism, and sociability
    top_intelligence = CustomUser.objects.order_by("-intelligence")
    top_athleticism = CustomUser.objects.order_by("-athleticism")
    top_sociability = CustomUser.objects.order_by("-sociability")

    intelligence_position = 1
    athleticism_position = 1
    sociability_position = 1

    #Iterates through sorted intelligence users to find the users position 
    for dbuser in top_intelligence:
        if dbuser.username == user.username:
            break
        intelligence_position += 1
    
    #Iterates through sorted athleticism users to find the users position 
    for dbuser in top_athleticism:
        if dbuser.username == user.username:
            break
        athleticism_position += 1
    
    #Iterates through sorted sociability users to find the users position 
    for dbuser in top_sociability:
        if dbuser.username == user.username:
            break
        sociability_position += 1
    
    return intelligence_position, athleticism_position, sociability_position


def compare_positions(user_lat, user_long, event_lat, event_long):
    """
    Function to compare the position and get the absolute distance between a
    the users current position and the position of the event

    Keyword arguments:
    user_lat -- current latitude of the user
    user_long -- current longitude of the user
    event_lat -- latitude of the event
    event_long -- longitude of the event

    Return:
    Distance between user and event
    """
    #Calculates and returns the absolute distance between the two sets of coordinates
    return sqrt( (user_lat - event_lat)**2 + (user_long - event_long)**2 )

def user_occupied(user):
    """
    Function to determine if a user is already occupied and registered to an event taking place
    at the current time.

    Keyword arguments:
    user -- User to check if occupied

    Return:
    Boolean indicating if a user is already currently signed up to an event
    """
    current_time = timezone.now() #Gets the current datetime
    #Iterates through events
    for event in Event.objects.all():  
        #If event is a battle then ignore the time constraint
        if event.type == "Battle":
            continue
        #Else checks if user is in the event and if the event is taking place within the current time
        minutes = int(60 * event.duration)
        if user in event.members.all() and event.date - timedelta(minutes=10) <= current_time <= event.date + timedelta(minutes=minutes):
            return True
    
    return False

def image_cost(image):
    """
    Function to return the cost of an image based on its rarity.

    Keyword arguments:
    image -- image to check the cost of
    """

    image_rarity = image.rarity #Gets the rarity of the image

    #If statements to determine price based on rarity
    if image_rarity == "Common":
        return 15
    elif image_rarity == "Uncommon":
        return 30
    elif image_rarity == "Rare":
        return 60
    elif image_rarity == "Epic":
        return 400
    elif image_rarity == "Legendary":
        return 1200
    else:
        return -1 #Error catching (Should never throw)
