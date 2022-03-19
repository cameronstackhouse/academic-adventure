from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Society

class CustomUserAdmin(UserAdmin):
    """
    Custom user admin to allow for the extended user attributes
    to be displayed on the admin.py page.
    """
    #Fields in the creation form
    fieldsets = (
        *UserAdmin.fieldsets, #Fields in the default user admin page
        (
            'Custom user fields',
            {
                'fields':(
                    "gamekeeper", #Field to determine if a user is a gamekeeper
                    #Can be used to set gamekeepers in the system
                ),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin) #Registers custom user with admin
admin.site.register(Event) #Registers event with admin
admin.site.register(Society) #Registers society with admin