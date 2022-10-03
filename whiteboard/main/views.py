import django.core.exceptions as exceptions
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email, validate_slug
from . import models

# Create your views here.

@require_http_methods(["GET"])
@login_required(login_url="signin")
def index(request):
    return render(request, "index.html")
    
@require_http_methods(["POST", "GET"])
def signin(request):
    if request.method == "POST":
        
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            username = get_user_model().objects.get(email=email)
        except exceptions.ObjectDoesNotExist:
            messages.info(request, "user not found")
            redirect("signin")
        
        user = authenticate(username=username, email=email, password=password)

        if user is None:
            messages.info(request, "user not found")
            redirect("signin")
            
        login(request, user=user)
        return redirect('index')
    
    else:
        return render(request, "signin.html")
    
@require_http_methods(["GET"])
@login_required(login_url="signin")
def signout(request):
    logout(request)
    return render(request, "signout.html")
   
@require_http_methods(["POST", "GET"]) 
def register(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        try:
            validate_slug(username)
        except exceptions.ValidationError:
            messages.info(request, "Not a valid username")
            return redirect('register')
        
        try:
            validate_slug(password)
        except exceptions.ValidationError:
            messages.info(request, "Not a valid password")
            return redirect('register')
        
        try:
            validate_email(email)
        except exceptions.ValidationError:
            messages.info(request, "Not a valid E-Mail")
            return redirect('register')
        
        #All data is valid
        if get_user_model().objects.filter(email=email).exists():
            messages.info(request, "E-Mail already taken")
            return redirect('register')
            
        user = get_user_model().objects.create_user(
                email=email,
                username=username, 
                password=password, 
                )
        user.save()
        client = models.Client(user=user)
        client.save()
        
        login(request, user=user)
        return redirect('index')
    
    else:
        return render(request, "register.html")
   
@require_http_methods(["POST", "GET"]) 
def invite(request: HttpRequest, code):
    
    #TODO: code gets matched with a board via the AuthenticationLink tabel in models.py
    # then the user dicites whether he want to log in (if he is not authenticated) or if he want to create a temp account
    # this works via AnonnymousClient (models.py) and the session libary in which data can be stored inside the server for a specific client
    # 
    # the goal is that this method is safe enough that there is no password required to access the board
    # if this is not possible we can work with the board method in views.py where you can access to every single board via the primary key
    
    return HttpResponse(code)

@login_required(login_url="signin")
@require_http_methods(["POST", "GET"])
def add_board(request):
    if request.method == "POST":
        name = request.POST["name"]
        
        if request.user.client.boards.filter(name=name).exists():
            messages.info(request, "name already used")
            return redirect('add_board')
        
        board = models.Board.objects.create(name=name)
        board.save()
        board.add_client(client=request.user.client, permission=models.Participation.OWNER)
        board.save()

        return redirect('boards')
    
    return render(request, "addBoard.html")
      
@require_http_methods(["GET"])
@login_required(login_url="signin")
def boards(request: HttpRequest):
    list = []
    for board in request.user.client.boards.all():
        dic = {}
        dic['name'] = board.name
        dic['permission'] = board.get_permission_label(request.user.client)
        list.append(dic)
    
    return render(request, "boards.html", {"boards" : str(list)})  

@require_http_methods(["GET"])
@login_required(login_url="signin")
def board(request: HttpRequest, id):
    
    # can only be ac

    obj = get_object_or_404(request.user.client.boards, pk=id)
    return HttpResponse(f"worked {obj}")
    
    # gives 
    