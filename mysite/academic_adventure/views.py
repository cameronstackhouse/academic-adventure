from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World!")

def home(request):
    return render(request, 'academic_adventure/home.html', )
