from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import TeachingAssistantProfile, MataKuliah
from authentication.views import ta_required, admin_required
from rekapanLog.views import get_month_rencana,get_all_rencana
from periode.models import Periode, PeriodeSekarang
# Create your views here.
@ta_required
def fill_profile(request):
    if request.method == 'POST':
        ta_profile = TeachingAssistantProfile(
            user = request.user,
            nama = request.POST.get('nama'),
            kontrak = request.POST.get('kontrak'),
            status = request.POST.get('status'),
            prodi = request.POST.get('prodi'),
            bulan_mulai = request.POST.get('bulan_mulai'),
            bulan_selesai = request.POST.get('bulan_selesai')
        )
        ta_profile.save()
        return redirect(reverse("main:homepage"))
    
    context = {
        'kontrak_choices': TeachingAssistantProfile.kontrak.field.choices,
        'status_choices': TeachingAssistantProfile.status.field.choices,
        'prodi_choices': TeachingAssistantProfile.prodi.field.choices,
        'bulan_choices': TeachingAssistantProfile.bulan_mulai.field.choices,
        'matkul_choices': MataKuliah.objects.order_by('nama')
    }

    return render(request, 'accounts/fill_profile.html', context)

@ta_required
def profile(request, id):
    profile = TeachingAssistantProfile.objects.get(user=id)
    context = {
        'profile': profile
    }

    # for x in range(len(profile.get_bulan())):
    #     print(profile.get_bulan()[x])
    print(profile.get_bulan())
    return render(request, 'accounts/profile.html', context)

@admin_required
def dashboard_eval(request):
    
    filter_kontrak = request.GET.getlist("kontrak")
    filter_status = request.GET.getlist("status")
    filter_prodi = request.GET.getlist("prodi")
    filter_matkul = request.GET.getlist("matkul")
    filter_statuslog = request.GET.get("statuslog",'all')
    kontrak_choices = TeachingAssistantProfile.kontrak.field.choices
    status_choices = TeachingAssistantProfile.status.field.choices
    prodi_choices = TeachingAssistantProfile.prodi.field.choices
    matkul_choices = MataKuliah.objects.order_by('nama')
    periode_sekarang = PeriodeSekarang.objects.all()
    ta_list = TeachingAssistantProfile.objects.filter(periode=periode_sekarang[0].periode)
    if(len(filter_kontrak) != 0) :
        for kontrak in kontrak_choices :
            if not (kontrak[1] in filter_kontrak):
                ta_list = ta_list.exclude(kontrak = kontrak[1])
    if len(filter_status) !=0 :
        for status in status_choices :
            if not (status[1] in filter_status):
                ta_list = ta_list.exclude(status= status[1])
    if len(filter_prodi) != 0 :
        for prodi in prodi_choices :
            if not (prodi[1] in filter_prodi):
                ta_list = ta_list.exclude(prodi = prodi[1])
    if len(filter_matkul) != 0:
        for matkul in matkul_choices :
            if not (matkul.nama in filter_matkul):
                ta_list = ta_list.exclude(daftar_matkul__id = matkul.id)
    

    rekap = []
    choice = "Rata-rata"
    bulan = request.GET.get("bulan","Rata-rata")    
    print(request.POST)
    if bulan == "Rata-rata":
        for i in ta_list:
            try :
                temp = get_all_rencana(i.user,TeachingAssistantProfile.objects.get(user=i.user),periode_sekarang[0].periode)
            except :
                temp = {}
            total = 0
            cnt = 0
            for value in temp.values() :
                if cnt >= 6 :
                    if value != None :
                        total += value
                cnt += 1
            if (i.kontrak == "Part Time"):
                rekap.append((total,20-total))
            else :
                rekap.append((total,40-total))
            
    else:
        for i in ta_list:
            try :
                temp = get_month_rencana(i.user,TeachingAssistantProfile.objects.get(user=i.user),periode_sekarang[0].periode)
            except :
                temp = {}
            total = 0
            cnt = 0
            for value in temp.values() :
                if cnt >= 6 :
                    if value != None :
                        total += value
                cnt += 1
            if (i.kontrak == "Part Time"):
                rekap.append((total,20-total))
            else :
                rekap.append((total,40-total))
        choice = bulan
    temp = zip(ta_list,rekap)

    context = {
        'ta_list': temp,
        'choice' : choice,
        'kontrak_choices': kontrak_choices,
        'status_choices': status_choices,
        'prodi_choices': prodi_choices,
        'matkul_choices': matkul_choices,
        'filter_kontrak':filter_kontrak,
        'filter_status':filter_status,
        'filter_prodi':filter_prodi,
        'filter_matkul':filter_matkul,
        'filter_statuslog':filter_statuslog,
    }
    
    return render(request, 'accounts/dashboard_eval.html', context)
