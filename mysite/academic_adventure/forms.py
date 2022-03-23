from django import forms
from .models import Event


class CreateForm(forms.ModelForm):
    """
    Form to create an event.
    Extends forms.ModelForm to use the django default form to create an object
    """
    class Meta:
        """
        Defines what should be shown in the form
        """
        model = Event #Selects model to use 
        #Input fields needed to create an event
        fields = ["name", "description", "date", "duration", "type", "longitude", "latitude"]
        #Labels for each input field
        labels = {"date": "Date and Time", #Date of the event
                  "duration": "Duration (Hours)", #Duration of the event
                  "longitude": "Longitude (Select from map)", #Location of the event
                  "latitude": "Latitude (Select from map)",
                  "name": "Name of event", #Name of the event
                  "type": "Type of event", #Type of event (Academic, Battle, Social, Sports)
                  "description": "Description of event"} #Description of the event
        
        #Widgets for the input boxes
        widgets = {
            "date": forms.DateTimeInput(attrs={"type":"datetime-local"}), #Adds a datetime picker to the date and time box
            "description": forms.Textarea(attrs={'rows': 3}),
        }