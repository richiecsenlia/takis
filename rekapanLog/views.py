from django.shortcuts import render
from pengisianLog.models import LogTA
from django.db.models import Sum, Avg
from django.db.models import Q, FloatField
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.views import ta_required, admin_required
from periode.models import Periode, PeriodeSekarang
from django.urls import reverse_lazy
from accounts.models import TeachingAssistantProfile
from pengisianLog.models import LogTA
from periode.models import PeriodeSekarang,Periode
from django.db.models.functions import Coalesce

def get_all_rencana(user_, profile, periode):
    rekapan_total = {"total_plan" : 0,                     
    "persiapan_plan" : 0,
    "penyelenggaraan_plan" : 0,
    "dukungan_plan" : 0,
    "pengembangan_plan" : 0,
    "riset_plan" : 0,
    "total_real" : 0,
    "persiapan_real" : 0,
    "penyelenggaraan_real" : 0,
    "dukungan_real" : 0,
    "pengembangan_real" : 0,
    "riset_real" : 0}

    lama_kontrak = len(profile.get_bulan())
    
    for month in profile.get_bulan():
        rekapan_per_bulan = get_month_rencana(user_,profile,periode,month) 

        rekapan_total["persiapan_plan"] += float(rekapan_per_bulan["persiapan_plan"])
        rekapan_total["penyelenggaraan_plan"] += float(rekapan_per_bulan["penyelenggaraan_plan"])
        rekapan_total["dukungan_plan"] += float(rekapan_per_bulan["dukungan_plan"])
        rekapan_total["pengembangan_plan"] += float(rekapan_per_bulan["pengembangan_plan"])
        rekapan_total["riset_plan"] += float(rekapan_per_bulan["riset_plan"])
        rekapan_total["persiapan_real"] += float(rekapan_per_bulan["persiapan_real"])
        rekapan_total["penyelenggaraan_real"] += float(rekapan_per_bulan["penyelenggaraan_real"])
        rekapan_total["dukungan_real"] += float(rekapan_per_bulan["dukungan_real"])
        rekapan_total["pengembangan_real"] += float(rekapan_per_bulan["pengembangan_real"])
        rekapan_total["riset_real"] += float(rekapan_per_bulan["riset_real"])
    
    rekapan_total["persiapan_plan"] = rekapan_total["persiapan_plan"]/lama_kontrak
    rekapan_total["penyelenggaraan_plan"] = rekapan_total["penyelenggaraan_plan"]/lama_kontrak
    rekapan_total["dukungan_plan"] = rekapan_total["dukungan_plan"]/lama_kontrak
    rekapan_total["pengembangan_plan"] = rekapan_total["pengembangan_plan"]/lama_kontrak
    rekapan_total["riset_plan"] = rekapan_total["riset_plan"]/lama_kontrak
    rekapan_total["persiapan_real"] = rekapan_total["persiapan_real"]/lama_kontrak
    rekapan_total["penyelenggaraan_real"] = rekapan_total["penyelenggaraan_real"]/lama_kontrak
    rekapan_total["dukungan_real"] = rekapan_total["dukungan_real"]/lama_kontrak
    rekapan_total["pengembangan_real"] = rekapan_total["pengembangan_real"]/lama_kontrak
    rekapan_total["riset_real"] = rekapan_total["riset_real"]/lama_kontrak
    
    rekapan_total["total_plan"] = rekapan_total["persiapan_plan"] + rekapan_total["penyelenggaraan_plan"] + rekapan_total["dukungan_plan"] + rekapan_total["pengembangan_plan"] + rekapan_total["riset_plan"]
    rekapan_total["total_real"] = rekapan_total["persiapan_real"] + rekapan_total["penyelenggaraan_real"] + rekapan_total["dukungan_real"] + rekapan_total["pengembangan_real"] + rekapan_total["riset_real"]
           
    return rekapan_total

def get_month_rencana(user_, profile, periode, month):
    list_periode = [periode]
    if(periode.semester == "Pendek"):
        tahun_start, tahun_end = periode.tahun_ajaran.split('/')
        sem_ganjil = tahun_end + "/" +str((int(tahun_end)+1))
        
        try:
            list_periode.append(Periode.objects.get(tahun_ajaran=periode.tahun_ajaran,semester="Genap"))
        except:
            pass
        try:    
            list_periode.append(Periode.objects.get(tahun_ajaran=sem_ganjil,semester="Ganjil"))
        except:
            pass
        
    elif(periode.semester == "Ganjil"):
        tahun_start, tahun_end = periode.tahun_ajaran.split('/')
        sem_pendek = str((int(tahun_start)-1)) + "/" +tahun_start
        try:
            list_periode.append(Periode.objects.get(tahun_ajaran=sem_pendek,semester="Pendek"))
        except:
            pass
    elif(periode.semester == "Genap"):
        try:
            list_periode.append(Periode.objects.get(tahun_ajaran=periode.tahun_ajaran,semester="Pendek"))
        except:
            pass
    rekapBulan_total = {}
    rekapBulan_total["persiapan_plan"] = 0
    rekapBulan_total["penyelenggaraan_plan"] = 0
    rekapBulan_total["dukungan_plan"] = 0
    rekapBulan_total["pengembangan_plan"]= 0
    rekapBulan_total["riset_plan"]= 0
    rekapBulan_total["persiapan_real"] = 0
    rekapBulan_total["penyelenggaraan_real"] =0
    rekapBulan_total["dukungan_real"] = 0
    rekapBulan_total["pengembangan_real"] = 0
    rekapBulan_total["riset_real"] = 0
    rekapBulan_total["total_plan"]= 0
    rekapBulan_total['total_real']= 0
    
    for i in list_periode :
        periode = i
        rekapBulan = LogTA.objects.aggregate(
            persiapan_plan=Coalesce(Sum("jam_kerja_rencana", filter=Q(periode_log=periode,user=user_,kategori='Persiapan Kuliah', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            penyelenggaraan_plan=Coalesce(Sum("jam_kerja_rencana", filter=Q(periode_log=periode,user=user_,kategori='Penyelenggaraan Kuliah', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            dukungan_plan=Coalesce(Sum("jam_kerja_rencana", filter=Q(periode_log=periode,user=user_,kategori='Dukungan Kuliah Kakak Asuh', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            pengembangan_plan=Coalesce(Sum("jam_kerja_rencana", filter=Q(periode_log=periode,user=user_,kategori='Pengembangan Institusi', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            riset_plan=Coalesce(Sum("jam_kerja_rencana", filter=Q(periode_log=periode,user=user_,kategori='Riset dan Pusilkom', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            persiapan_real=Coalesce(Sum("jam_kerja_realisasi", filter=Q(periode_log=periode,user=user_,kategori='Persiapan Kuliah', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            penyelenggaraan_real=Coalesce(Sum("jam_kerja_realisasi", filter=Q(periode_log=periode,user=user_,kategori='Penyelenggaraan Kuliah', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            dukungan_real=Coalesce(Sum("jam_kerja_realisasi", filter=Q(periode_log=periode,user=user_,kategori='Dukungan Kuliah Kakak Asuh', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            pengembangan_real=Coalesce( Sum("jam_kerja_realisasi", filter=Q(periode_log=periode,user=user_,kategori='Pengembangan Institusi', bulan_pengerjaan=month)),0.0,output_field=FloatField()), 
            riset_real=Coalesce( Sum("jam_kerja_realisasi", filter=Q(periode_log=periode,user=user_,kategori='Riset dan Pusilkom', bulan_pengerjaan=month)),0.0,output_field=FloatField()))
        
        if month in profile.get_bulan():
            rekapKontrak = get_month_rencana(user_, profile, periode, "Sepanjang Kontrak")
            rekapBulan["persiapan_plan"] += float(rekapKontrak["persiapan_plan"] or 0.0)
            rekapBulan["penyelenggaraan_plan"] += float(rekapKontrak["penyelenggaraan_plan"] or 0.0)
            rekapBulan["dukungan_plan"] += float(rekapKontrak["dukungan_plan"] or 0.0)
            rekapBulan["pengembangan_plan"]+= float(rekapKontrak["pengembangan_plan"] or 0.0)
            rekapBulan["riset_plan"]+= float(rekapKontrak["riset_plan"] or 0.0)
            rekapBulan["persiapan_real"] += float(rekapKontrak["persiapan_real"] or 0.0)
            rekapBulan["penyelenggaraan_real"] += float(rekapKontrak["penyelenggaraan_real"] or 0.0)
            rekapBulan["dukungan_real"] += float(rekapKontrak["dukungan_real"] or 0.0)
            rekapBulan["pengembangan_real"] += float(rekapKontrak["pengembangan_real"] or 0.0)
            rekapBulan["riset_real"] += float(rekapKontrak["riset_real"] or 0.0)
        
        if month in periode.get_bulan():
            rekapKontrak = get_month_rencana(user_, profile, periode, "Semester Kuliah")
            rekapBulan["persiapan_plan"] += float(rekapKontrak["persiapan_plan"] or 0.0)
            rekapBulan["penyelenggaraan_plan"] += float(rekapKontrak["penyelenggaraan_plan"] or 0.0)
            rekapBulan["dukungan_plan"] += float(rekapKontrak["dukungan_plan"] or 0.0)
            rekapBulan["pengembangan_plan"]+= float(rekapKontrak["pengembangan_plan"] or 0.0)
            rekapBulan["riset_plan"]+= float(rekapKontrak["riset_plan"] or 0.0)
            rekapBulan["persiapan_real"] += float(rekapKontrak["persiapan_real"] or 0.0)
            rekapBulan["penyelenggaraan_real"] += float(rekapKontrak["penyelenggaraan_real"] or 0.0)
            rekapBulan["dukungan_real"] += float(rekapKontrak["dukungan_real"] or 0.0)
            rekapBulan["pengembangan_real"] += float(rekapKontrak["pengembangan_real"] or 0.0)
            rekapBulan["riset_real"] += float(rekapKontrak["riset_real"] or 0.0)


        rekapBulan["total_plan"] = rekapBulan["persiapan_plan"] + rekapBulan["penyelenggaraan_plan"] + rekapBulan["dukungan_plan"] + rekapBulan["pengembangan_plan"] + rekapBulan["riset_plan"]
        rekapBulan["total_real"] = rekapBulan["persiapan_real"] + rekapBulan["penyelenggaraan_real"] + rekapBulan["dukungan_real"] + rekapBulan["pengembangan_real"] + rekapBulan["riset_real"]

        rekapBulan_total["persiapan_plan"] += rekapBulan["persiapan_plan"]
        rekapBulan_total["penyelenggaraan_plan"] += rekapBulan["penyelenggaraan_plan"]
        rekapBulan_total["dukungan_plan"] += rekapBulan["dukungan_plan"]
        rekapBulan_total["pengembangan_plan"]+= rekapBulan["pengembangan_plan"]
        rekapBulan_total["riset_plan"]+= rekapBulan["riset_plan"]
        rekapBulan_total["persiapan_real"] += rekapBulan["persiapan_real"]
        rekapBulan_total["penyelenggaraan_real"] += rekapBulan["penyelenggaraan_real"]
        rekapBulan_total["dukungan_real"] += rekapBulan["dukungan_real"]
        rekapBulan_total["pengembangan_real"] += rekapBulan["pengembangan_real"]
        rekapBulan_total["riset_real"] += rekapBulan["riset_real"]
        rekapBulan_total["total_plan"]+= rekapBulan['total_plan']
        rekapBulan_total['total_real']+= rekapBulan['total_real']

    return rekapBulan_total

@login_required(login_url=reverse_lazy("authentication:login"))
def rekap_page(request, name):
    profile = TeachingAssistantProfile.objects.get(user=User.objects.get(username=name))
    periode_sekarang = PeriodeSekarang.objects.get(univ = request.user.univ.univ).periode

    if request.method == 'GET':
        rekapAvg = get_all_rencana(User.objects.get(username=name),profile,periode_sekarang)
        rekapAvg["choice"] = "Rata-rata"

    else:
        bulan = request.POST.get("bulan")
        work = {}

        if bulan == "Rata-rata":
            rekapAvg = get_all_rencana(User.objects.get(username=name),profile,periode_sekarang)
            rekapAvg["choice"] = "Rata-rata"
        else:
            rekapAvg = get_month_rencana(User.objects.get(username=name), profile, periode_sekarang, bulan)
            rekapAvg["choice"] = bulan

    return render(request, "rekap_log.html", rekapAvg)

