from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Society

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom user fields',
            {
                'fields':(
                    "gamekeeper",
                ),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin) #Registers custom user with admin
admin.site.register(Event) #Registers event with admin
admin.site.register(Society) #Registers society with admin