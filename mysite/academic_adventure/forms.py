from django import forms
from .models import Event

class CreateForm(forms.ModelForm):
    """Form to create an event"""
    class Meta:
        model = Event #Selects model to use 
        #Input fields
        fields = ["longitude", "latitude", "name", "description", "host", "date", "duration", "type", "society"]
        #Lables for each input field
        labels = {"date": "Date and Time (YYYY-MM-DD HH:MM:SS)",
                  "duration": "Duration (Hours)",
                  "longitude": "Longitude (Select from map)",
                  "latitude": "Latitude (Select from map)",
                  "name": "Name of event",
                  "host": "Host of event",
                  "type": "Type of event",
                  "society": "Society running the event",
                  "description": "Description of event"}