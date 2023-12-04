from django.forms import ModelForm
from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UnivChoices
class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan password anda'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan ulang password anda'}))
    univ = forms.ModelChoiceField(
            queryset=UnivChoices.objects.all()
        )
    class Meta:
        model = User
        fields = ['username','univ', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan username anda'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan email anda'}),
            'univ' :forms.Select()
        }
    
class PasswordForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan password baru anda'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan ulang password baru anda'}))
    class Meta:
        model = User
        fields = ['password1','password2']