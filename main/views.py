from django.shortcuts import render
from django.views.decorators.http import require_GET

# Create your views here.
@require_GET
def homepage(request):
    return render(request, "homepage.html")