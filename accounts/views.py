from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import TeachingAssistantProfile, MataKuliah
from authentication.views import ta_required, admin_required
from rekapanLog.views import get_month_rencana,get_all_rencana
# Create your views here.
@ta_required
def fill_profile(request):
    if request.method == 'POST':
        ta_profile = TeachingAssistantProfile(
            user = request.user,
            nama = request.POST.get('nama'),
            kontrak = request.POST.get('kontrak'),
            status = request.POST.get('status'),
            prodi = request.POST.get('prodi')
        )
        ta_profile.save()
        return redirect(reverse("main:homepage"))
    
    context = {
        'kontrak_choices': TeachingAssistantProfile.kontrak.field.choices,
        'status_choices': TeachingAssistantProfile.status.field.choices,
        'prodi_choices': TeachingAssistantProfile.prodi.field.choices,
        'matkul_choices': MataKuliah.objects.order_by('nama')
    }

    return render(request, 'accounts/fill_profile.html', context)

@ta_required
def profile(request, id):
    profile = TeachingAssistantProfile.objects.get(user=id)
    context = {
        'profile': profile
    }
    
    return render(request, 'accounts/profile.html', context)

@admin_required
def dashboard_eval(request):
    ta_list = TeachingAssistantProfile.objects.all()
    context = {
        'ta_list': ta_list
    }
    rekap = []
    choice = "Rata-rata"
    if request.method == 'GET':
        for i in ta_list:
            temp = get_all_rencana(i.user)
            total = 0
            print(temp)
            for value in temp.values() :
                if value != None :
                    total += value
            if (i.kontrak == "Part Time"):
                rekap.append((total,20-total))
            else :
                rekap.append((tota,40-total))
        

    else:
        bulan = request.POST.get("bulan")

        if bulan == "Rata-rata":
            for i in ta_list:
                
                temp = get_all_rencana(i.user)
                total = 0
                for value in temp.values() :
                    if value != None :
                        total += value
                if (i.kontrak == "Part Time"):
                    rekap.append((total,20-total))
                else :
                    rekap.append((tota,40-total))
            
        else:
            for i in ta_list:
                
                temp = get_month_rencana(i.user,bulan)
                total = 0
                for value in temp.values() :
                    if value != None :
                        total += value
                if (i.kontrak == "Part Time"):
                    rekap.append((total,20-total))
                else :
                    rekap.append((tota,40-total))
            choice = bulan
    temp = zip(ta_list,rekap)
    context = {
        'ta_list': temp,
        'choice' : choice
    }

    return render(request, 'accounts/dashboard_eval.html', context)
