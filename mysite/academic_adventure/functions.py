from datetime import timedelta
from math import sqrt
from django.utils import timezone
from .models import CustomUser, Event, Image

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

def populate_with_images():
    """
    Populates the database with the pre made profile pictures.
    """
    
    if not Image.objects.exists(): #If no images in the database
        #Populates the database with the initial profile pictures
        Image.objects.create(name="Ronald", img="profilepics/1.png", icon="profilepics/icon1.png", rarity="Common", in_store=True)
        Image.objects.create(name="Niamh", img="profilepics/2.png", icon="profilepics/icon2.png", rarity="Common", in_store=True)
        Image.objects.create(name="Roger", img="profilepics/3.png", icon="profilepics/icon3.png", rarity="Common", in_store=True)
        Image.objects.create(name="Trini", img="profilepics/4.png", icon="profilepics/icon4.png", rarity="Common", in_store=True)
        Image.objects.create(name="Walter", img="profilepics/5.png", icon="profilepics/icon5.png", rarity="Common", in_store=True)
        Image.objects.create(name="Stacey", img="profilepics/6.png", icon="profilepics/icon6.png", rarity="Common", in_store=True)
        Image.objects.create(name="Billy", img="profilepics/7.png", icon="profilepics/icon7.png", rarity="Common", in_store=True)
        Image.objects.create(name="Layla", img="profilepics/8.png", icon="profilepics/icon8.png", rarity="Common", in_store=True)
        Image.objects.create(name="James", img="profilepics/9.png", icon="profilepics/icon9.png", rarity="Common", in_store=True)
        Image.objects.create(name="Laina", img="profilepics/10.png", icon="profilepics/icon10.png", rarity="Common", in_store=True)
        Image.objects.create(name="Hector", img="profilepics/11.png", icon="profilepics/icon11.png", rarity="Common", in_store=True)
        Image.objects.create(name="Olivia", img="profilepics/12.png", icon="profilepics/icon12.png", rarity="Common", in_store=True)
        Image.objects.create(name="Brian", img="profilepics/13.png", icon="profilepics/icon13.png", rarity="Common", in_store=True)
        Image.objects.create(name="Wu", img="profilepics/14.png", icon="profilepics/icon14.png", rarity="Common", in_store=True)
        Image.objects.create(name="Raul", img="profilepics/15.png", icon="profilepics/icon15.png", rarity="Common", in_store=True)
        Image.objects.create(name="Lucius", img="profilepics/16.png", icon="profilepics/icon16.png", rarity="Common", in_store=True)
        Image.objects.create(name="Richard", img="profilepics/17.png", icon="profilepics/icon17.png", rarity="Legendary", in_store=True)
        Image.objects.create(name="Bella", img="profilepics/18.png", icon="profilepics/icon18.png", rarity="Uncommon", in_store=True)
        Image.objects.create(name="Cat", img="profilepics/19.png", icon="profilepics/icon19.png", rarity="Epic", in_store=True)
        Image.objects.create(name="Dog", img="profilepics/20.png", icon="profilepics/icon20.png", rarity="Rare", in_store=True)
        Image.objects.create(name="Avatar-tron 3000", img="profilepics/21.png", icon="profilepics/icon21.png", rarity="Rare", in_store=True)
        Image.objects.create(name="Greg", img="profilepics/22.png", icon="profilepics/icon22.png", rarity="Epic", in_store=True)
        Image.objects.create(name="Bunny", img="profilepics/23.png", icon="profilepics/icon23.png", rarity="Rare", in_store=True)
        Image.objects.create(name="Frog", img="profilepics/24.png", icon="profilepics/icon24.png", rarity="Epic", in_store=True)


def populate_unique_images():
    Image.objects.create(name="Laison", img="profilepics/laison.png", icon="profilepics/iconlaison.png", rarity="Legendary", in_store=False)
    Image.objects.create(name="Cameron", img="profilepics/cameron.png", icon="profilepics/iconcameron.png", rarity="Legendary", in_store=False)
    Image.objects.create(name="Simon", img="profilepics/simon.png", icon="profilepics/iconsimon.png", rarity="Legendary", in_store=False)
    Image.objects.create(name="Leo", img="profilepics/leo.png", icon="profilepics/iconleo.png", rarity="Legendary", in_store=False)
    Image.objects.create(name="Andrew", img="profilepics/andrew.png", icon="profilepics/iconandrew.png", rarity="Legendary", in_store=False)
    Image.objects.create(name="Mattis", img="profilepics/mattis.png", icon="profilepics/iconmattis.png", rarity="Legendary", in_store=False)



