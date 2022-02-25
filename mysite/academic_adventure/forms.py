from django import forms
from .models import Event

class CreateForm(forms.ModelForm):
    """Form to create an event"""
    class Meta:
        model = Event 
        fields = ["longitude", "latitude", "name", "host", "date", "duration", "type", "society"]
        labels = ["Longitude", "Latitude", "Name", "Host", "Date", "Duration", "Type", "Society"]
