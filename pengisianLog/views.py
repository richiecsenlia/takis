from django.shortcuts import render
from .models import LogTA

# Create your views here.
def daftarLogTA(request):
    log = LogTA.objects.filter(user=request.user)
    context = {'log': log}
    return render(request, 'daftarLogTA.html', context)

def daftarLogEvaluator(request):
    log = LogTA.objects.all()
    context = {'log': log}
    return render(request, 'daftarLogEvaluator.html', context)