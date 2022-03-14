from django import forms
from .models import Event


class CreateForm(forms.ModelForm):
    """Form to create an event"""
    class Meta:
        model = Event #Selects model to use 
        #Input fields
        fields = ["longitude", "latitude", "name", "description", "date", "duration", "type", "society"]
        #Labels for each input field
        labels = {"date": "Date and Time",
                  "duration": "Duration (Hours)",
                  "longitude": "Longitude (Select from map)",
                  "latitude": "Latitude (Select from map)",
                  "name": "Name of event",
                  "type": "Type of event",
                  "society": "Society running the event",
                  "description": "Description of event"}
        
        widgets = {
            "date": forms.DateTimeInput(attrs={"type":"datetime-local"}), #Adds a datetime picker to the date and time box
        }