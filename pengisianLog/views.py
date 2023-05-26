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
from django.db.models import Q
from django.contrib.auth.models import User
from accounts.models import TeachingAssistantProfile, MataKuliah
from periode.models import PeriodeSekarang,Periode

VALUE_ERROR = "Input tidak valid"
URL_DAFTAR_LOG_TA = "pengisianLog:daftar_log_ta"
URL_DASHBOARD = "accounts:dashboard_eval"

def count_jam_kerja(profile,periode_sekarang,periode,jumlah_rencana_kinerja,bobot_jam_rencana_kinerja):
    print(periode_sekarang.get_bulan())
    semester_kuliah_divider = (len(periode_sekarang.get_bulan()))*4
    sepanjang_kontrak_divider = (len(profile.get_bulan()))*4

    jam_kerja = 0
    if periode == "Semester Kuliah":
        jam_kerja = (jumlah_rencana_kinerja*bobot_jam_rencana_kinerja)/semester_kuliah_divider
    elif periode == "Sepanjang Kontrak":
        jam_kerja = (jumlah_rencana_kinerja*bobot_jam_rencana_kinerja)/sepanjang_kontrak_divider
    else:
        jam_kerja = (jumlah_rencana_kinerja*bobot_jam_rencana_kinerja)/4
    return jam_kerja


@ta_required
def form_log_ta(request):
    try:
        if request.method == 'GET':
            profile = TeachingAssistantProfile.objects.get(user=request.user)
            
            return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
                'periode_choice': LogTA.periode.field.choices, 
                'bulan_choice': LogTA.bulan_pengerjaan.field.choices,
                'matkul_choice': [matkul.nama for matkul in profile.daftar_matkul.all()]})
        else:
            profile = TeachingAssistantProfile.objects.get(user=request.user)
            periode_sekarang = PeriodeSekarang.objects.get().periode

            jumlah_realisasi_kinerja_validasi = 0
            bobot_jam_realisasi_kinerja_validasi = 0
            if (request.POST.get('jumlah_realisasi_kinerja')) == "":
                 jumlah_realisasi_kinerja_validasi = 0
                 bobot_jam_realisasi_kinerja_validasi = 0
            else:
                jumlah_realisasi_kinerja_validasi = int(request.POST.get('jumlah_realisasi_kinerja'))
                bobot_jam_realisasi_kinerja_validasi = float(request.POST.get('bobot_realisasi_kinerja'))

            user = request.user
            kategori = request.POST.get('kategori')
            jenis_pekerjaan = request.POST.get('pekerjaan')
            detail_kegiatan = request.POST.get('detail_kegiatan')
            pemberi_tugas = request.POST.get('pemberi_tugas')
            uraian = request.POST.get('uraian')
            matkul = MataKuliah.objects.get(nama=request.POST.get('matkul'))
            periode = request.POST.get('periode')
            bulan_pengerjaan = request.POST.get('bulan_pengerjaan')
            jumlah_rencana_kinerja = int(request.POST.get('jumlah_kinerja'))
            satuan_rencana_kinerja = request.POST.get('satuan_kinerja')
            bobot_jam_rencana_kinerja = float(request.POST.get('bobot_kinerja'))
            jam_kerja_rencana = float(count_jam_kerja(profile,periode_sekarang,periode,jumlah_rencana_kinerja,bobot_jam_rencana_kinerja))
            jumlah_realisasi_kinerja = jumlah_realisasi_kinerja_validasi
            satuan_realisasi_kinerja = request.POST.get('satuan_realisasi_kinerja')
            bobot_jam_realisasi_kinerja = bobot_jam_realisasi_kinerja_validasi
            jam_kerja_realisasi = float(count_jam_kerja(profile,periode_sekarang,periode,jumlah_realisasi_kinerja,bobot_jam_realisasi_kinerja))
            periode_log = periode_sekarang

            LogTA.objects.create(
                user=user,
                kategori=kategori,
                jenis_pekerjaan=jenis_pekerjaan,
                detail_kegiatan=detail_kegiatan,
                pemberi_tugas=pemberi_tugas,
                uraian=uraian,
                matkul=matkul,
                periode=periode,
                bulan_pengerjaan=bulan_pengerjaan,
                jumlah_rencana_kinerja=jumlah_rencana_kinerja,
                satuan_rencana_kinerja=satuan_rencana_kinerja,
                bobot_jam_rencana_kinerja=bobot_jam_rencana_kinerja,
                jam_kerja_rencana=jam_kerja_rencana,
                jumlah_realisasi_kinerja=jumlah_realisasi_kinerja,
                satuan_realisasi_kinerja=satuan_realisasi_kinerja,
                bobot_jam_realisasi_kinerja=bobot_jam_realisasi_kinerja,
                jam_kerja_realisasi=jam_kerja_realisasi,
                periode_log=periode_log,
            )
            return redirect(reverse(URL_DAFTAR_LOG_TA))
    except ValueError:
        messages.error(request, VALUE_ERROR)
        profile = TeachingAssistantProfile.objects.get(user=request.user)
        return render(request, 'form_log.html', {'kategori_choice': LogTA.kategori.field.choices, 
                'periode_choice': LogTA.periode.field.choices, 
                'bulan_choice': LogTA.bulan_pengerjaan.field.choices,
                'matkul_choice': [matkul.nama for matkul in profile.daftar_matkul.all()]})
    
@login_required(login_url=reverse_lazy('authentication:login'))
def edit_log_ta(request, id):
    try:
        log = LogTA.objects.get(pk=id)
        profile = TeachingAssistantProfile.objects.get(user=log.user)
        periode_sekarang = PeriodeSekarang.objects.get().periode


        context = {'log': log,
                'kategori_choice': [kategori for kategori in LogTA.kategori.field.choices if log.kategori not in kategori], 
                'periode_choice': [periode for periode in LogTA.periode.field.choices if log.periode not in periode], 
                'bulan_choice': [bulan_pengerjaan for bulan_pengerjaan in LogTA.bulan_pengerjaan.field.choices if log.bulan_pengerjaan not in bulan_pengerjaan],
                'matkul_choice': [matkul.nama for matkul in profile.daftar_matkul.all() if log.matkul.nama not in matkul.nama]}

        if request.method == 'GET':
            return render(request, 'edit_log.html', context)
        else:
            jumlah_realisasi_kinerja_validasi = 0
            bobot_jam_realisasi_kinerja_validasi = 0
            if (request.POST.get('jumlah_realisasi_kinerja')) == "":
                 jumlah_realisasi_kinerja_validasi = 0
                 bobot_jam_realisasi_kinerja_validasi = 0
            else:
                jumlah_realisasi_kinerja_validasi = int(request.POST.get('jumlah_realisasi_kinerja'))
                bobot_jam_realisasi_kinerja_validasi = float(request.POST.get('bobot_realisasi_kinerja'))

            log.user = log.user
            log.kategori = request.POST.get('kategori')
            log.jenis_pekerjaan = request.POST.get('pekerjaan')
            log.detail_kegiatan = request.POST.get('detail_kegiatan')
            log.pemberi_tugas = request.POST.get('pemberi_tugas')
            log.uraian = request.POST.get('uraian')
            log.matkul = MataKuliah.objects.get(nama=request.POST.get('matkul'))
            log.periode = request.POST.get('periode')
            log.bulan_pengerjaan = request.POST.get('bulan_pengerjaan')
            log.jumlah_rencana_kinerja = int(request.POST.get('jumlah_kinerja'))
            log.satuan_rencana_kinerja = request.POST.get('satuan_kinerja')
            log.bobot_jam_rencana_kinerja = float(request.POST.get('bobot_kinerja'))
            log.jam_kerja_rencana = float(count_jam_kerja(profile,periode_sekarang,log.periode,log.jumlah_rencana_kinerja,log.bobot_jam_rencana_kinerja))
            log.jumlah_realisasi_kinerja = jumlah_realisasi_kinerja_validasi
            log.satuan_realisasi_kinerja = request.POST.get('satuan_realisasi_kinerja')
            log.bobot_jam_realisasi_kinerja = bobot_jam_realisasi_kinerja_validasi
            log.jam_kerja_realisasi = float(count_jam_kerja(profile,periode_sekarang,log.periode,log.jumlah_realisasi_kinerja,log.bobot_jam_realisasi_kinerja))
            log.save()

            if str(request.user.role) == 'admin':
                return redirect(reverse("accounts:dashboard_eval"))
            return redirect(reverse(URL_DAFTAR_LOG_TA))
    except ValueError:
        messages.error(request, VALUE_ERROR)
        return render(request, 'edit_log.html', context)

@login_required(login_url=reverse_lazy('authentication:login'))
def delete_log_ta(request, id):
    log = LogTA.objects.get(pk=id)
    log.delete()

    if str(request.user.role) == 'admin':
                return redirect(reverse("accounts:dashboard_eval"))
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

def exclude_matkul(filter_matkul,logs,matkul_choices):
    if len(filter_matkul) != 0:
        for matkul in matkul_choices:
            if not (matkul.nama in filter_matkul):
                logs = logs.exclude(matkul__id = matkul.id)
    return logs

@ta_required
def daftar_log_ta(request):
    
    periode_sekarang_all = PeriodeSekarang.objects.all()
    periode_sekarang = periode_sekarang_all[0].periode
    filter_bulan = request.GET.getlist("bulan")
    filter_kategori = request.GET.getlist("kategori")
    filter_periode = request.GET.getlist("periode")
    filter_term = request.GET.get("term",periode_sekarang.id)
    filter_matkul = request.GET.getlist("matkul")
    logs = LogTA.objects.filter(Q(user=request.user, periode_log=filter_term))
    term = request.user.teachingassistantprofile.periode_set.all()
    kategori_choice = LogTA.kategori.field.choices 
    periode_choice = LogTA.periode.field.choices
    bulan_choice = LogTA.bulan_pengerjaan.field.choices
    matkul_choices = MataKuliah.objects.order_by('nama')

    logs = exclude_bulan(filter_bulan, logs, bulan_choice)
    logs = exclude_kategori(filter_kategori, logs, kategori_choice)
    logs = exclude_periode(filter_periode, logs, periode_choice)
    print(logs)
    logs = exclude_matkul(filter_matkul,logs,matkul_choices)
    print(logs)
    bulan = datetime.now().month
    print(bulan_choice[bulan-1][0])
    print(periode_sekarang)
    
    rekap = get_month_rencana(request.user,TeachingAssistantProfile.objects.get(user=request.user),periode_sekarang,bulan_choice[bulan-1][0])
    
    # rekap = get_month_rencana(request.user, bulan_choice[bulan-1][0],periode_sekarang)
    print(rekap)
    total = rekap['total_real']
    
    if request.user.teachingassistantprofile.kontrak == 'Part Time':
        defisit = 20 - total
    else :
        defisit = 40 - total
    filter_term = Periode.objects.get(id=filter_term)
    print("aa",matkul_choices)
    context = {'logs': logs,
                'kategori_choice': kategori_choice, 
                'periode_choice': periode_choice, 
                'bulan_choice': bulan_choice,
                'matkul_choices':matkul_choices,
                'filter_bulan':filter_bulan,
                'filter_kategori':filter_kategori,
                'filter_periode':filter_periode,
                'filter_matkul':filter_matkul,
                'defisit':defisit,
                'total':total,
                'term':term,
                'current':filter_term}
    return render(request, 'daftar_log.html', context)

@require_GET
@admin_required
def daftar_log_evaluator(request,username):
    periode_sekarang_all = PeriodeSekarang.objects.all()
    periode_sekarang = periode_sekarang_all[0].periode
    filter_bulan = request.GET.getlist("bulan")
    filter_kategori = request.GET.getlist("kategori")
    filter_periode = request.GET.getlist("periode")
    filter_term = request.GET.get("term",periode_sekarang.id)
    logs = LogTA.objects.filter(Q(periode_log=filter_term,user__username=username)).order_by('user', 'id')
    
    kategori_choice = LogTA.kategori.field.choices 
    periode_choice = LogTA.periode.field.choices
    bulan_choice = LogTA.bulan_pengerjaan.field.choices
    logs = exclude_bulan(filter_bulan, logs, bulan_choice)
    logs = exclude_kategori(filter_kategori, logs, kategori_choice)
    logs = exclude_periode(filter_periode, logs, periode_choice)
        
    term = User.objects.get(username=username).teachingassistantprofile.periode_set.all()

    filter_term = Periode.objects.get(id=filter_term)

    context = {'logs': logs,
                'kategori_choice': kategori_choice, 
                'periode_choice': periode_choice, 
                'bulan_choice': bulan_choice,
                'filter_bulan':filter_bulan,
                'filter_kategori':filter_kategori,
                'filter_periode':filter_periode,
                'term':term,
                'current':filter_term}
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
