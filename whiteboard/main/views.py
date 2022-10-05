import django.core.exceptions as exceptions
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email, validate_slug
from . import models

# Create your views here.

@require_http_methods(["GET"])
@login_required(login_url="signin")
def index_view(request):
    return render(request, "index.html")
    
@require_http_methods(["POST", "GET"])
def signin_view(request):
    if request.method == "POST":
        
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = authenticate(email=email, password=password)

        if user is None:
            messages.info(request, "user not found")
            redirect("signin")
            
        login(request, user=user)
        return redirect('index')
    
    else:
        return render(request, "signin.html")
    
@require_http_methods(["GET"])
@login_required(login_url="signin")
def signout_view(request):
    logout(request)
    return render(request, "signout.html")
   
@require_http_methods(["POST", "GET"]) 
def register_view(request):
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
def invite_view(request: HttpRequest, code):
    

    return HttpResponse(code)

@login_required(login_url="signin")
@require_http_methods(["POST", "GET"])
def add_board_view(request):
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
def boards_view(request: HttpRequest):
    board_list = []
    for board in request.user.client.boards.all():
        dic = {}
        dic['name'] = board.name
        dic['permission'] = board.get_permission_label(request.user.client)
        board_list.append(dic)
    
    return render(request, "boards.html", {"boards" : str(board_list)})  

@require_http_methods(["GET"])
@login_required(login_url="signin")
def board_view(request: HttpRequest, id):

    obj = get_object_or_404(request.user.client.boards, pk=id)
    return HttpResponse(f"worked {obj}")

    