from math import sqrt
from .models import CustomUser

def get_user_positions(user):
    """
    Function to get the users positions in the leaderboard rankings. 
    This is used to display the users position to them.

    :param user: user to find positions of
    :return: users positions in the leaderboards of points
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
    """
    #Calculates and returns the absolute distance between the two sets of coordinates
    return sqrt( (user_lat - event_lat)**2 + (user_long - event_long)**2 )
