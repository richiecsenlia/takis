from django.shortcuts import render
from .models import LogTA

# Create your views here.
def daftarLogTA(request, userID):
    log = LogTA.objects.all()
    context = {'log': log}
    return render(request, 'daftarLogTA.html', context)

def daftarLogEvaluator(request):
    log = LogTA.objects.all()
    context = {'log': log}
    return render(request, 'daftarLogEvaluator.html', context)