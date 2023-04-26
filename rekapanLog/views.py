from django.shortcuts import render
from pengisianLog.models import LogTA
from django.db.models import Sum, Avg
from django.db.models import Q
from authentication.views import ta_required, admin_required

# Create your views here.
def get_all_rencana(user_):
    aggr = LogTA.objects.aggregate(persiapan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Persiapan Kuliah'))/6, 
        penyelenggaraan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Penyelenggaraan Kuliah'))/6,
        dukungan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Dukungan Kuliah Kakak Asuh'))/6,
        pengembangan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Pengembangan Institusi'))/6,
        riset_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Riset dan Pusilkom'))/6,
        persiapan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Persiapan Kuliah'))/6, 
        penyelenggaraan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Penyelenggaraan Kuliah'))/6,
        dukungan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Dukungan Kuliah Kakak Asuh'))/6,
        pengembangan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Pengembangan Institusi'))/6,
        riset_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Riset dan Pusilkom'))/6) 
    
    return aggr

def get_month_rencana(user_, month):
    rekapBulan = LogTA.objects.aggregate(persiapan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Persiapan Kuliah', bulan_pengerjaan=month)), 
        penyelenggaraan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Penyelenggaraan Kuliah', bulan_pengerjaan=month)),
        dukungan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Dukungan Kuliah Kakak Asuh', bulan_pengerjaan=month)),
        pengembangan_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Pengembangan Institusi', bulan_pengerjaan=month)),
        riset_plan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Riset dan Pusilkom', bulan_pengerjaan=month)),
        persiapan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Persiapan Kuliah', bulan_pengerjaan=month)), 
        penyelenggaraan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Penyelenggaraan Kuliah', bulan_pengerjaan=month)),
        dukungan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Dukungan Kuliah Kakak Asuh', bulan_pengerjaan=month)),
        pengembangan_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Pengembangan Institusi', bulan_pengerjaan=month)),
        riset_real=Sum("konversi_jam_realisasi_kinerja", filter=Q(kategori='Riset dan Pusilkom', bulan_pengerjaan=month))) 
    
    return rekapBulan

@ta_required
def rekap_page(request, name):
    rekapAvg = get_all_rencana(name)
    rekapAvg["choice"] = "Rata-rata"

    return render(request, "rekap_log.html", rekapAvg)