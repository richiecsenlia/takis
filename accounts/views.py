from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import TeachingAssistantProfile, MataKuliah
from authentication.views import ta_required, admin_required

# Create your views here.
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
def profile(request, slug):
    profile = TeachingAssistantProfile.objects.get(slug=slug)
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

    return render(request, 'accounts/dashboard_eval.html', context)
