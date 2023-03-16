from django.forms import ModelForm
from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.Form):
    username = forms.CharField(label='username', min_length=0, max_length=150)
    password = forms.CharField(label='password', widget=forms.PasswordInput)
class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
    
class PasswordForm(ModelForm):
    class Meta:
        model = User
        fields = ['password']