from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib import messages

def register(request):
    """
    View to register a user in the database for the application

    Keyword arguments:
    request -- HttpRequest of the user
    """
    form = RegisterForm() #Default user creation form provided by django
    if request.method == "POST": #Checks if POST request
        credentials = RegisterForm(request.POST) #If so gets users entered credentials
        if credentials.is_valid(): #Checks if the users password and username is valid
            credentials.save() #If so save the username and password to the database
            messages.success(request, "Account created") #Add a success message to the screen
            return redirect("/register") #Redirects to the register page, where the user waits 3 seconds and then gets redirected to login page
        else:
            messages.error(request, "Error, password or username invalid.") #Display error message

    return render(request, 'register/register.html', {'form':form}) #Displays register HTML form with the Django user registration form
    
def privacy(request):
    """
    View to show the user the privacy policy for the application

    Keyword arguments:
    request -- HttpRequest of the user
    """
    return render(request, 'register/privacy-policy.html') #Renders the privacy policy HTML template
