from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy

from accounts.forms import TAProfileForm
from accounts.models import TeachingAssistantProfile, MataKuliah
from authentication.views import ta_required, admin_required
from periode.models import Periode, PeriodeSekarang
from rekapanLog.views import get_month_rencana,get_all_rencana

def apply_filter(ta_list, filter_list, choices, field_name):
    if len(filter_list) != 0:
        for choice in choices:
            if choice[1] not in filter_list:
                ta_list = ta_list.exclude(**{field_name: choice[1]})
    return ta_list

def process_ta_list(ta_list, period, month=None):
    rekap = []
    for i in ta_list:
        if month:
            temp = get_month_rencana(i.user, TeachingAssistantProfile.objects.get(user=i.user), period, month)
        else:
            temp = get_all_rencana(i.user, TeachingAssistantProfile.objects.get(user=i.user), period)
        
        total = temp['total_real']
        kontrak_limit = 20 if i.kontrak == "Part Time" else 40
        rekap.append((total, kontrak_limit - total))
        
    return rekap

# Create your views here.
@ta_required
def fill_profile(request):
    form = TAProfileForm()
    try:
        if request.user.teachingassistantprofile != None:
            return redirect(reverse("main:homepage"))
    except ObjectDoesNotExist:
        if request.method == 'POST':
            form = TAProfileForm(request.POST)
            if form.is_valid():
                new_profile = form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                for matkul in form.cleaned_data['daftar_matkul']:
                    new_profile.daftar_matkul.add(matkul)
                return redirect(reverse("main:homepage"))
    context = {
        'form': form
    }

    return render(request, 'accounts/fill_profile.html', context)


@login_required(login_url=reverse_lazy('authentication:login'))
def profile(request, id):
    profile = TeachingAssistantProfile.objects.get(user=id)
    context = {
        'profile': profile
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required(login_url=reverse_lazy('authentication:login'))
def edit_profile(request, id):
    form = TAProfileForm()
    profile = get_object_or_404(TeachingAssistantProfile, user=id)

    form.fields['nama'].initial = profile.nama
    form.fields['kontrak'].initial = profile.kontrak
    form.fields['prodi'].initial = profile.prodi
    form.fields['status'].initial = profile.status
    form.fields['bulan_mulai'].initial = profile.bulan_mulai
    form.fields['tahun_mulai'].initial = profile.tahun_mulai
    form.fields['bulan_selesai'].initial = profile.bulan_selesai
    form.fields['tahun_selesai'].initial = profile.tahun_selesai
    form.fields['daftar_matkul'].initial = [matkul for matkul in profile.daftar_matkul.all()]
    
    if request.method == 'POST':
        form = TAProfileForm(request.POST)
        if form.is_valid():
            profile.nama = form.cleaned_data['nama']
            profile.kontrak = form.cleaned_data['kontrak']
            profile.prodi = form.cleaned_data['prodi']
            profile.status = form.cleaned_data['status']
            profile.bulan_mulai = form.cleaned_data['bulan_mulai']
            profile.tahun_mulai = form.cleaned_data['tahun_mulai']
            profile.bulan_selesai = form.cleaned_data['bulan_selesai']
            profile.tahun_selesai = form.cleaned_data['tahun_selesai']
            profile.save()
            for matkul in form.cleaned_data['daftar_matkul']:
                profile.daftar_matkul.add(matkul)
            return redirect(reverse("accounts:profile", kwargs={'id': profile.user.id}))

    context = {
        'form': form,
        'profile': profile
    }

    return render(request, 'accounts/edit_profile.html', context)


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
    periode_str = f"Periode {periode_sekarang[0].periode}"
    bulan_choice = periode_sekarang[0].periode.get_bulan()
    print(bulan_choice)
    ta_list = apply_filter(ta_list, filter_kontrak, kontrak_choices, 'kontrak')
    ta_list = apply_filter(ta_list, filter_status, status_choices, 'status')
    ta_list = apply_filter(ta_list, filter_prodi, prodi_choices, 'prodi')
    ta_list = apply_filter(ta_list, filter_matkul, matkul_choices, 'matkul')
    
    rekap = []
    choice = "Rata-rata"
    bulan = request.GET.get("bulan","Rata-rata")
    
    if bulan == "Rata-rata":
        rekap = process_ta_list(ta_list, periode_sekarang[0].periode)
    else:
        rekap = process_ta_list(ta_list, periode_sekarang[0].periode, bulan)
        choice = bulan
    
    temp = zip(ta_list, rekap)

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
        'periode_sekarang': periode_str,
        'bulan_choices':bulan_choice
    }
    
    return render(request, 'accounts/dashboard_eval.html', context)
