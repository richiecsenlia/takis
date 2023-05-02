from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.
@require_GET
@login_required(login_url=reverse_lazy("authentication:login"))
def homepage(request):
    return render(request, "homepage.html")