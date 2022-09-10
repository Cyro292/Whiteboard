from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.



@login_required(login_url='signin')
def index(request):
    return render(request, "index.html",  
        {"message": "hey"
        })

def signin(request):
    return render(request, "signin.html")

@login_required(login_url='signin')
def signout(request):
    return render(request, "signout.html")
