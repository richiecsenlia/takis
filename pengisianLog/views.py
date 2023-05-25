from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from authentication.views import admin_required, ta_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_GET
from pengisianLog.models import LogTA
from datetime import datetime
from rekapanLog.views import get_month_rencana,get_all_rencana

VALUE_ERROR = "Input tidak valid"
URL_DAFTAR_LOG_TA = "pengisianLog:daftar_log_ta"

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
            return redirect(reverse(URL_DAFTAR_LOG_TA))
    except ValueError:
        messages.error(request, VALUE_ERROR)
        return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
                'periode_choice': LogTA.periode.field.choices, 
                'bulan_choice': LogTA.bulan_pengerjaan.field.choices})
    
@login_required(login_url=reverse_lazy('authentication:login'))
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
            return redirect(reverse(URL_DAFTAR_LOG_TA))
    except ValueError:
        messages.error(request, VALUE_ERROR)
        return render(request, 'edit_log.html', context)

@login_required(login_url=reverse_lazy('authentication:login'))
def delete_log_ta(request, id):
    log = LogTA.objects.get(pk=id)
    log.delete()
    return redirect(reverse(URL_DAFTAR_LOG_TA))

def exclude_periode(filter_periode, logs, periode_choice):
    if len(filter_periode) != 0 :
        for periode in periode_choice :
            if periode[1] not in filter_periode:
                logs = logs.exclude(periode = periode[1])
    return logs

def exclude_kategori(filter_kategori, logs, kategori_choice):
    if len(filter_kategori) !=0 :
        for kategori in kategori_choice :
            if kategori[1] not in filter_kategori:
                logs = logs.exclude(kategori= kategori[1])
    return logs

def exclude_bulan(filter_bulan, logs, bulan_choice):
    if(len(filter_bulan) != 0) :
        for bulan in bulan_choice :
            if bulan[1] not in filter_bulan:
                logs = logs.exclude(bulan_pengerjaan = bulan[1])
    return logs

@ta_required
def daftar_log_ta(request):
    
    filter_bulan = request.GET.getlist("bulan")
    filter_kategori = request.GET.getlist("kategori")
    filter_periode = request.GET.getlist("periode")
    
    logs = LogTA.objects.filter(user=request.user)
    
    kategori_choice = LogTA.kategori.field.choices 
    periode_choice = LogTA.periode.field.choices
    bulan_choice = LogTA.bulan_pengerjaan.field.choices
    logs = exclude_bulan(filter_bulan, logs, bulan_choice)
    logs = exclude_kategori(filter_kategori, logs, kategori_choice)
    logs = exclude_periode(filter_periode, logs, periode_choice)
    bulan = datetime.now().month
    print(bulan_choice[bulan-1][0])
    rekap = get_month_rencana(request.user, bulan)
    total = 0
    cnt = 0
    for key in rekap:
        if cnt >= 6 :
            if rekap[key] != None :
                total = rekap[key]
        cnt += 1
    
    if request.user.teachingassistantprofile.kontrak == 'Part Time':
        defisit = 20 - total
    else :
        defisit = 40 - total
    context = {'logs': logs,
                'kategori_choice': kategori_choice, 
                'periode_choice': periode_choice, 
                'bulan_choice': bulan_choice,
                'filter_bulan':filter_bulan,
                'filter_kategori':filter_kategori,
                'filter_periode':filter_periode,
                'defisit':defisit,
                'total':total}
    return render(request, 'daftar_log.html', context)

@require_GET
@admin_required
def daftar_log_evaluator(request,username):
    print(request.GET)
    filter_bulan = request.GET.getlist("bulan")
    filter_kategori = request.GET.getlist("kategori")
    filter_periode = request.GET.getlist("periode")
    logs = LogTA.objects.filter(user__username=username).order_by('user', 'id')
    
    kategori_choice = LogTA.kategori.field.choices 
    periode_choice = LogTA.periode.field.choices
    bulan_choice = LogTA.bulan_pengerjaan.field.choices
    logs = exclude_bulan(filter_bulan, logs, bulan_choice)
    logs = exclude_kategori(filter_kategori, logs, kategori_choice)
    logs = exclude_periode(filter_periode, logs, periode_choice)
        
    context = {'logs': logs,
                'kategori_choice': kategori_choice, 
                'periode_choice': periode_choice, 
                'bulan_choice': bulan_choice,
                'filter_bulan':filter_bulan,
                'filter_kategori':filter_kategori,
                'filter_periode':filter_periode}
    return render(request, 'daftar_log.html', context)

@require_GET
@login_required
def detail_log(request, id):
    log = LogTA.objects.get(pk=id)
    
    if str(request.user.role) != 'admin' and log.user != request.user:
        raise PermissionDenied

    context = {'log': log}
    return render(request, 'detail_log.html', context)

@login_required(login_url=reverse_lazy("authentication:login"))
def history_log_ta(request, id):
    log = get_object_or_404(LogTA, id=id)
    if log.user != request.user and str(request.user.role) != 'admin':
        raise PermissionDenied

    context = {
        'history': log.history.all()
    }

    return render(request, 'history_log.html', context)
