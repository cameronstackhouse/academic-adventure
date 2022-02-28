from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Society

admin.site.register(CustomUser, UserAdmin) #Registers custom user with admin
admin.site.register(Event) #Registers event with admin
admin.site.register(Society) #Registers society with admin