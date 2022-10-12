import django.core.exceptions as exceptions
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from . import models, forms

# Create your views here.

@require_http_methods(["GET"])
@login_required(login_url="signin")
def index_view(request):
    return render(request, "index.html")
    
@require_http_methods(["POST", "GET"])
def signin_view(request):
    
    form = forms.LoginForm()
    if request.method == "POST":
        
        form = forms.LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(email=email, password=password)

            if user is None:
                messages.info(request, "user not found")
                redirect("signin")
                
            login(request, user=user)
            return redirect('index')
    
    return render(request, "signin.html", {'form': form})
    
@require_http_methods(["GET"])
@login_required(login_url="signin")
def signout_view(request):
    logout(request)
    return render(request, "signout.html")
   
@require_http_methods(["POST", "GET"]) 
def register_view(request):
    form = forms.RegisterForm()
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        
        if form.is_valid():       
                
            user= form.save(commit=True)
        
            login(request, user=user)
            return redirect('index')

    
    return render(request, "register.html", {'form': form})
   
@require_http_methods(["POST", "GET"]) 
def invite_view(request: HttpRequest, code):
    

    return HttpResponse(code)

@login_required(login_url="signin")
@require_http_methods(["POST", "GET"])
def add_board_view(request):
    form = forms.AddBoardFrom()
    if request.method == "POST":
        form = forms.AddBoardFrom(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            
            if request.user.boards.filter(name=name).exists():
                messages.info(request, "name already used")
                return redirect('add_board')
            
            board = models.Board.objects.create(name=name)
            board.add_user(user=request.user, permission=models.Participation.OWNER)

            return redirect('boards')
    
    return render(request, "addBoard.html", {'form': form})
      
@require_http_methods(["GET"])
@login_required(login_url="signin")
def boards_view(request: HttpRequest):
    board_list = []
    for board in request.user.boards.all():
        dic = {}
        dic['name'] = board.name
        dic['permission'] = board.get_permission_label(request.user)
        board_list.append(dic)
    
    return render(request, "boards.html", {"boards" : str(board_list)})  

@require_http_methods(["GET"])
@login_required(login_url="signin")
def board_view(request: HttpRequest, id):

    obj = get_object_or_404(request.user.boards, pk=id)
    return HttpResponse(f"worked {obj}")
    