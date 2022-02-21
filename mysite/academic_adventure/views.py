from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello")

def home(request):
    return render(request, 'academic_adventure/home.html')
