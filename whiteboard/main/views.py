from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "index.html")

def view_login(request):
    return HttpResponse("Upcoming")

def view_logout(request):
    return HttpResponse("Upcoming logout")
