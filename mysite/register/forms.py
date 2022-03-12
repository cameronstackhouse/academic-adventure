from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class RegisterForm(UserCreationForm): 
    """
    Custom user registration form for users registering for the application.

    Extends UserCreationForm to use the default Django user creation form, which
    deals with invalid user input without requiring extra code.
    """
    def __init__(self, *args, **kwargs): 
        """
        Constructor for the user creation form.
        
        Methods contained within here are used to change the
        input boxes and their requirements
        """
        super().__init__(*args, **kwargs) #Inherits fields from the UserCreationForm

        #Customises the username input field
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'username', 
            'id':'username', #Sets id for easy css manuipulation
            'type':'text', 
            'placeholder':'username', 
            'maxlength': '16', #Sets a maximum username length
            'minlength': '6', #Sets a minimum username length
            }) 
        #Customises the first password input field
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password1', 
            'id':'password1', #Sets id for easy css manuipulation
            'type':'password', 
            'placeholder':'password', 
            'maxlength':'22',  
            'minlength':'8' #Sets a minimum password length, ensures security
            }) 
        #Customises the second password input field
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password2', 
            'id':'password2', #Sets id for easy css manuipulation
            'type':'password', 
            'placeholder':'confirm password', 
            'maxlength':'22',  
            'minlength':'8' #Sets a minimum password length, ensures security
            }) 
 
 
    username = forms.CharField(max_length=20, label=False) #Changes the username input field

    class Meta:
        """
        Defines what fields are in the form to create a new user
        """
        model = User #Uses the default user model to create a new user
        fields = ["username", "password1", "password2"] #Sets the fields of the form