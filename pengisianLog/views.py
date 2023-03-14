from django.shortcuts import render

from authentication.views import ta_required, admin_required
from .models import LogTA

# Create your views here.
def daftarLogTA(request):
    logs = LogTA.objects.filter(user=request.user)
    context = {'logs': logs}
    return render(request, 'daftarLogTA.html', context)

def daftarLogEvaluator(request):
    logs = LogTA.objects.all()
    context = {'logs': logs}
    return render(request, 'daftarLogEvaluator.html', context)