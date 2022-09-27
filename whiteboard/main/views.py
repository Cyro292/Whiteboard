from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from . import models

# Create your views here.

@login_required(login_url="signin")
def index(request):
    return render(request, "index.html")
    
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user=user)
            return redirect('index')
        
        messages.info(request, "user not found")
    
    return render(request, "signin.html")
    
@login_required(login_url="signin")
def signout(request):
    logout(request)
    return render(request, "signout.html")
    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        
        if not get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.create_user(
                    username=username, 
                    password=password, 
                    email=email)
            user.save()
        
            login(request, user=user)
            return redirect('index')
        
        messages.info(request, "username already taken")
        return redirect('register')
    
    return render(request, "register.html")
    
def invite(request: HttpRequest, code):
    
    #TODO: code gets matched with a board via the AuthenticationLink tabel in models.py
    # then the user dicites whether he want to log in (if he is not authenticated) or if he want to create a temp account
    # this works via AnonnymousClient (models.py) and the session libary in which data can be stored inside the server for a specific client
    # 
    # the goal is that this method is safe enough that there is no password required to access the board
    # if this is not possible we can work with the board method in views.py where you can access to every single board via the primary key
    
    return HttpResponse(code)

def add_board(request):
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]
        
        board = models.Board(name=name, password=password)
        board.add_client(client=request.user.client, permission=models.Participation.OWNER)
        board.save()
        return render(request, "addBoard.html")
    
    return render(request, "addBoard.html")
        

def board(request: HttpRequest, id):
    
    # can only be ac
    
    try: 
        request.user.client.boards.get(pk=id)
        return HttpResponse("true")
    except models.ObjectDoesNotExist: 
        raise Http404("Object dose not exist")
    
    # gives 
    