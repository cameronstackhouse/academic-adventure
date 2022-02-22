from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #Used to reject user entry to web page if not logged in

@login_required
def home(request):
    return render(request, 'academic_adventure/home.html')

