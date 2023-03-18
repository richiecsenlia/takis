from django.shortcuts import render

from authentication.views import ta_required, admin_required
from .models import LogTA

# Create your views here.
@ta_required
def daftarLogTA(request):
    logs = LogTA.objects.filter(user=request.user)
    context = {'logs': logs}
    return render(request, 'daftarLog.html', context)

@admin_required
def daftarLogEvaluator(request):
    logs = LogTA.objects.all()
    context = {'logs': logs}
    return render(request, 'daftarLog.html', context)