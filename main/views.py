from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from main.utils import detect_user

# Create your views here.
@login_required(login_url=reverse_lazy('authentication:login'))
def homepage_handler(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(reverse(redirect_url))
