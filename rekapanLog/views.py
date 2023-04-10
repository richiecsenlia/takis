from django.shortcuts import render
from pengisianLog.models import LogTA
from django.db.models import Sum, Avg
from django.db.models import Q

# Create your views here.
def get_all_rencana(user_):
    aggr = LogTA.objects.aggregate(persiapan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Persiapan Kuliah'))/6, 
        penyelenggaraan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Penyelenggaraan Kuliah'))/6,
        dukungan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Dukungan Kuliah Kakak Asuh'))/6,
        pengembangan=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Pengembangan Institusi'))/6,
        riset=Sum("konversi_jam_rencana_kinerja", filter=Q(kategori='Riset dan Pusilkom'))/6) 
    
    return aggr