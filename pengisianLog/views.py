from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def form_log_TA(request):
    return render(request, 'form_log.html', {})