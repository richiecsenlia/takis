from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import LogTA
from authentication.views import admin_required, ta_required, ta_role_check, admin_role_check
from django.urls import reverse
from authentication.views import ta_required, admin_required
from .models import LogTA

VALUE_ERROR = "Input tidak valid"

# Create your views here.
@ta_required
def form_log_TA(request):
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
            return redirect(reverse("pengisianLog:daftarLogTA"))
    except ValueError:
        messages.error(request, VALUE_ERROR)
        return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
                'periode_choice': LogTA.periode.field.choices, 
                'bulan_choice': LogTA.bulan_pengerjaan.field.choices})
    
@ta_required
def edit_log_ta(request, id):
    try:
        log = LogTA.objects.get(pk=id)

        context = {'log': log,
                'kategori_choice': [kategori for kategori in LogTA.kategori.field.choices if log.kategori not in kategori], 
                'periode_choice': [periode for periode in LogTA.periode.field.choices if log.periode not in periode], 
                'bulan_choice': [bulan_pengerjaan for bulan_pengerjaan in LogTA.bulan_pengerjaan.field.choices if log.bulan_pengerjaan not in bulan_pengerjaan]}

        if request.method == 'GET':
            return render(request, 'edit_log.html', context)
        else:
            jumlah_realisasi_kinerja_validasi = 0
            konversi_jam_realisasi_kinerja_validasi = 0
            if (request.POST.get('jumlah_realisasi_kinerja')) == "":
                 jumlah_realisasi_kinerja_validasi = 0
                 konversi_jam_realisasi_kinerja_validasi = 0
            else:
                jumlah_realisasi_kinerja_validasi = int(request.POST.get('jumlah_realisasi_kinerja'))
                konversi_jam_realisasi_kinerja_validasi = int(request.POST.get('jumlah_realisasi_kinerja')) / 4

            log.user = request.user
            log.kategori = request.POST.get('kategori')
            log.jenis_pekerjaan = request.POST.get('pekerjaan')
            log.detail_kegiatan = request.POST.get('detail_kegiatan')
            log.pemberi_tugas = request.POST.get('pemberi_tugas')
            log.uraian = request.POST.get('uraian')
            log.periode = request.POST.get('periode')
            log.bulan_pengerjaan = request.POST.get('bulan_pengerjaan')
            log.jumlah_rencana_kinerja = int(request.POST.get('jumlah_kinerja'))
            log.satuan_rencana_kinerja = request.POST.get('satuan_kinerja')
            log.konversi_jam_rencana_kinerja = int(request.POST.get('jumlah_kinerja')) / 4
            log.jumlah_realisasi_kinerja = jumlah_realisasi_kinerja_validasi
            log.satuan_realisasi_kinerja = request.POST.get('satuan_realisasi_kinerja')
            log.konversi_jam_realisasi_kinerja = konversi_jam_realisasi_kinerja_validasi
            log.save()
            return redirect(reverse("pengisianLog:daftarLogTA"))
    except ValueError:
        messages.error(request, VALUE_ERROR)
        return render(request, 'edit_log.html', context)

@ta_required
def delete_log_ta(request, id):
    log = LogTA.objects.get(pk=id)
    log.delete()
    return redirect(reverse("pengisianLog:daftarLogTA"))

@ta_required
def daftarLogTA(request):
    
    filter_bulan = request.GET.getlist("bulan")
    filter_kategori = request.GET.getlist("kategori")
    filter_periode = request.GET.getlist("periode")
    logs = LogTA.objects.filter(user=request.user)
    
    kategori_choice = LogTA.kategori.field.choices 
    periode_choice = LogTA.periode.field.choices
    bulan_choice = LogTA.bulan_pengerjaan.field.choices
    if(len(filter_bulan) != 0) :
        for bulan in bulan_choice :
            if not (bulan[1] in filter_bulan):
                logs = logs.exclude(bulan_pengerjaan = bulan[1])
    if len(filter_kategori) !=0 :
        for kategori in kategori_choice :
            if not (kategori[1] in filter_kategori):
                logs = logs.exclude(kategori= kategori[1])
    if len(filter_periode) != 0 :
        for periode in periode_choice :
            if not (periode[1] in filter_periode):
                logs = logs.exclude(periode = periode[1])
        
    context = {'logs': logs,
                'kategori_choice': kategori_choice, 
                'periode_choice': periode_choice, 
                'bulan_choice': bulan_choice,
                'filter_bulan':filter_bulan,
                'filter_kategori':filter_kategori,
                'filter_periode':filter_periode}
    return render(request, 'daftarLog.html', context)

@admin_required
def daftarLogEvaluator(request):
    print(request.GET)
    filter_bulan = request.GET.getlist("bulan")
    filter_kategori = request.GET.getlist("kategori")
    filter_periode = request.GET.getlist("periode")
    logs = LogTA.objects.all()
    
    kategori_choice = LogTA.kategori.field.choices 
    periode_choice = LogTA.periode.field.choices
    bulan_choice = LogTA.bulan_pengerjaan.field.choices
    if(len(filter_bulan) != 0) :
        for bulan in bulan_choice :
            if not (bulan[1] in filter_bulan):
                logs = logs.exclude(bulan_pengerjaan = bulan[1])
    if len(filter_kategori) !=0 :
        for kategori in kategori_choice :
            if not (kategori[1] in filter_kategori):
                logs = logs.exclude(kategori= kategori[1])
    if len(filter_periode) != 0 :
        for periode in periode_choice :
            if not (periode[1] in filter_periode):
                logs = logs.exclude(periode = periode[1])
        
    context = {'logs': logs,
                'kategori_choice': kategori_choice, 
                'periode_choice': periode_choice, 
                'bulan_choice': bulan_choice,
                'filter_bulan':filter_bulan,
                'filter_kategori':filter_kategori,
                'filter_periode':filter_periode}
    return render(request, 'daftarLog.html', context)
