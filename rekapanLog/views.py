from django.shortcuts import render
from pengisianLog.models import LogTA
from django.db.models import Sum, Avg
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.views import ta_required, admin_required
from periode.models import Periode, PeriodeSekarang
from django.urls import reverse_lazy

# Create your views here.
def get_all_rencana(user_, periode):
    aggr = LogTA.objects.aggregate(persiapan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Persiapan Kuliah', periode_log=periode))/6, 
        penyelenggaraan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Penyelenggaraan Kuliah', periode_log=periode))/6,
        dukungan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Dukungan Kuliah Kakak Asuh', periode_log=periode))/6,
        pengembangan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Pengembangan Institusi', periode_log=periode))/6,
        riset_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Riset dan Pusilkom', periode_log=periode))/6,
        persiapan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Persiapan Kuliah', periode_log=periode))/6, 
        penyelenggaraan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Penyelenggaraan Kuliah', periode_log=periode))/6,
        dukungan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Dukungan Kuliah Kakak Asuh', periode_log=periode))/6,
        pengembangan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Pengembangan Institusi', periode_log=periode))/6,
        riset_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Riset dan Pusilkom', periode_log=periode))/6) 
    
    return aggr

def get_month_rencana(user_, month, periode):
    rekapBulan = LogTA.objects.aggregate(persiapan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Persiapan Kuliah', bulan_pengerjaan=month, periode_log=periode)), 
        penyelenggaraan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Penyelenggaraan Kuliah', bulan_pengerjaan=month, periode_log=periode)),
        dukungan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Dukungan Kuliah Kakak Asuh', bulan_pengerjaan=month, periode_log=periode)),
        pengembangan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Pengembangan Institusi', bulan_pengerjaan=month, periode_log=periode)),
        riset_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(user=user_,kategori='Riset dan Pusilkom', bulan_pengerjaan=month, periode_log=periode)),
        persiapan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Persiapan Kuliah', bulan_pengerjaan=month, periode_log=periode)), 
        penyelenggaraan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Penyelenggaraan Kuliah', bulan_pengerjaan=month, periode_log=periode)),
        dukungan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Dukungan Kuliah Kakak Asuh', bulan_pengerjaan=month, periode_log=periode)),
        pengembangan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Pengembangan Institusi', bulan_pengerjaan=month, periode_log=periode)),
        riset_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(user=user_,kategori='Riset dan Pusilkom', bulan_pengerjaan=month, periode_log=periode))) 
    
    return rekapBulan

@login_required(login_url=reverse_lazy("authentication:login"))
def rekap_page(request, name):
    periode_sekarang = PeriodeSekarang.objects.all()
    if request.method == 'GET':
        rekapAvg = get_all_rencana(User.objects.get(username=name), periode_sekarang[0].periode)
        rekapAvg["choice"] = "Rata-rata"

    else:
        bulan = request.POST.get("bulan")
        work = {}

        if bulan == "Rata-rata":
            rekapAvg = get_all_rencana(User.objects.get(username=name), periode_sekarang[0].periode)
            rekapAvg["choice"] = "Rata-rata"
        else:
            rekapAvg = get_month_rencana(User.objects.get(username=name), bulan, periode_sekarang[0].periode)
            rekapAvg["choice"] = bulan

    return render(request, "rekap_log.html", rekapAvg)

