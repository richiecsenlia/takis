from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import LogTA
from authentication.views import admin_required, ta_required, ta_role_check, admin_role_check
from django.urls import reverse
from authentication.views import ta_required, admin_required
from .models import LogTA

# Create your views here.
@ta_required
def form_log_TA(request):
    try:
        if request.method == 'GET':
            return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
                'periode_choice': LogTA.periode.field.choices, 
                'bulan_choice': LogTA.bulan_pengerjaan.field.choices})
        else:
            LogTA.objects.create(
                user = request.user,
                kategori = request.POST.get('kategori'),
                jenis_pekerjaan = request.POST.get('pekerjaan'),
                detail_kegiatan = request.POST.get('detail_kegiatan'),
                pemberi_tugas = request.POST.get('pemberi_tugas'),
                uraian = request.POST.get('uraian'),
                periode = request.POST.get('periode'),
                bulan_pengerjaan = request.POST.get('bulan_pengerjaan'),
                jumlah_rencana_kinerja = int(request.POST.get('jumlah_kinerja')),
                satuan_rencana_kinerja = request.POST.get('satuan_kinerja'),
                konversi_jam_rencana_kinerja = int(request.POST.get('jam_rencana_kinerja'))
            )
            return redirect(reverse("pengisianLog:daftarLogTA"))
    except ValueError:
        return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
                'periode_choice': LogTA.periode.field.choices, 
                'bulan_choice': LogTA.bulan_pengerjaan.field.choices})

def daftarLogTA(request):
    logs = LogTA.objects.filter(user=request.user)
    context = {'logs': logs}
    return render(request, 'daftarLog.html', context)

@admin_required
def daftarLogEvaluator(request):
    logs = LogTA.objects.all()
    context = {'logs': logs}
<<<<<<< HEAD
    return render(request, 'daftarLogEvaluator.html', context)
=======
    return render(request, 'daftarLog.html', context)
>>>>>>> 512eee2823d894f44eb9370336d38ec85eb312aa
