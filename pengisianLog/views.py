from django.shortcuts import render, redirect
from .models import LogTA
from authentication.views import admin_required, ta_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from authentication.views import ta_required, admin_required
from django.views.decorators.http import require_GET
from pengisianLog.models import LogTA

# Create your views here.
@ta_required
def form_log_ta(request):
    try:
        if request.method == 'GET':
            return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
                'periode_choice': LogTA.periode.field.choices, 
                'bulan_choice': LogTA.bulan_pengerjaan.field.choices})
        else:
            jumlah_realisasi_kinerja_validasi = 0
            konversi_jam_realisasi_kinerja_validasi = 0
            if (request.POST.get('jumlah_realisasi_kinerja')) == "":
                 jumlah_realisasi_kinerja_validasi = 0
                 konversi_jam_realisasi_kinerja_validasi = 0
            else:
                 jumlah_realisasi_kinerja_validasi = int(request.POST.get('jumlah_realisasi_kinerja'))
                 konversi_jam_realisasi_kinerja_validasi = int(request.POST.get('jumlah_realisasi_kinerja')) / 4
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
                konversi_jam_rencana_kinerja = int(request.POST.get('jumlah_kinerja')) / 4,
                jumlah_realisasi_kinerja = jumlah_realisasi_kinerja_validasi,
                satuan_realisasi_kinerja = request.POST.get('satuan_realisasi_kinerja'),
                konversi_jam_realisasi_kinerja = konversi_jam_realisasi_kinerja_validasi
            )
            return redirect(reverse("pengisianLog:daftar_log_ta"))
    except ValueError:
        return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
                'periode_choice': LogTA.periode.field.choices, 
                'bulan_choice': LogTA.bulan_pengerjaan.field.choices})

@require_GET
@ta_required
def daftar_log_ta(request):
    logs = LogTA.objects.filter(user=request.user)
    context = {'logs': logs}
    return render(request, 'daftar_log.html', context)

@require_GET
@admin_required
def daftar_log_evaluator(request):
    logs = LogTA.objects.all().order_by('user', 'id')
    context = {'logs': logs}
    return render(request, 'daftar_log.html', context)

@require_GET
@login_required
def detail_log(request, id):
    log = LogTA.objects.get(pk=id)
    
    if str(log.user.role) != 'admin' and log.user != request.user:
        raise PermissionDenied

    context = {'log': log}
    return render(request, 'detail_log.html', context)
