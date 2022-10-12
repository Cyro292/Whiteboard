from django import forms
from . import models

class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.get_user_model()
        fields = ['email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
    
class LoginForm(forms.Form):
    
    email = forms.CharField(max_length=225)
    password = forms.CharField(max_length=225, widget=forms.PasswordInput())
        
class AddBoardFrom(forms.ModelForm):
    
    class Meta:
        model = models.Board
        fields = ['name', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
