from django.shortcuts import render
from django.http import HttpResponse
from .models import LogTA

# Create your views here.
def form_log_TA(request):
    return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
        'periode_choice': LogTA.periode.field.choices, 
        'bulan_choice': LogTA.bulan_pengerjaan.field.choices})