from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib import messages

def register(request):
    """View to register a user in the database
    """
    form = RegisterForm() #Default user creation form provided by django
    if request.method == "POST": #Checks if POST request
        credentials = RegisterForm(request.POST) #If so gets users entered credentials
        if credentials.is_valid(): #Checks if the users password and username is valid
            credentials.save() #If so save the username and password to the database
            messages.success(request, "Account created") #Add a success message to the screen
            return redirect("/register")
        else:
            messages.error(request, "Error, password or username invalid.") #Display error message

    return render(request, 'register/register.html', {'form':form}) #Displays register HTML form with generic Django user registration form
