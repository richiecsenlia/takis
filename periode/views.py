from django.shortcuts import redirect, render
from django.urls import reverse
from accounts.models import TeachingAssistantProfile
from authentication.views import admin_required

from periode.models import Periode, PeriodeSekarang
from .forms import PeriodeForm, PeriodeSekarangForm

# Create your views here.
@admin_required
def create_periode(request):
    if request.method == "POST":
        form = PeriodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("periode:edit-periode-sekarang"))

    else:
        form = PeriodeForm()

    return render(request, "buat_periode.html", {"form": form})

@admin_required
def edit_periode_sekarang(request):
    if request.method == "POST":
        form = PeriodeSekarangForm(request.POST)
        if form.is_valid():
            new = form.cleaned_data['periode']
            curr = PeriodeSekarang.objects.all()

            if curr.exists():
                curr.update(periode = new)
            else:
                curr = PeriodeSekarang(periode = new)
                curr.save()
            
            return redirect(reverse("periode:edit-periode-sekarang"))

    else:
        form = PeriodeSekarangForm()
        periode_sekarang = PeriodeSekarang.objects.all()
        initial = None if not periode_sekarang.exists() else periode_sekarang.first().periode
        form.fields['periode'].initial = initial

    return render(request, "edit_periode_sekarang.html", {"form": form})

@admin_required
def daftar_ta(request):
    daftar_ta = TeachingAssistantProfile.objects.all()
    periode_sekarang = PeriodeSekarang.objects.first()
    daftar_ta_aktif = periode_sekarang.periode.daftar_ta.all()
    pilihan_periode = Periode.objects.all()

    context = {'daftar_ta': daftar_ta,
               'daftar_ta_aktif': daftar_ta_aktif,
               'periode_sekarang': periode_sekarang,
               'pilihan_periode': pilihan_periode}
    return render(request, 'daftar_ta.html', context)

@admin_required
def assign_ta(request):
    daftar_ta = TeachingAssistantProfile.objects.all()
    pilihan_periode = Periode.objects.all()

    context = {'daftar_ta': daftar_ta,
               'pilihan_periode': pilihan_periode}
    return render(request, 'assign_ta.html', context)