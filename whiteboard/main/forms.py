from django import forms
from . import models

class RegisterForm(forms.Form):
    class Meta:
        model = models.get_user_model()
        fields = ['email', 'username', 'password']
    
class LoginForm(forms.Form):
    
    class Meta:
        model = models.get_user_model()
        fields = ['email', 'password']
        
class AddBoardFrom(forms.Form):
    
    class Meta:
        model = models.Board()
        fields = ['email', 'password']
