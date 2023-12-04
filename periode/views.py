from django.views.decorators.http import require_http_methods, require_GET
from django.shortcuts import redirect, render
from django.urls import reverse
from accounts.models import TeachingAssistantProfile
from authentication.views import admin_required
from django.http import HttpResponseRedirect

from periode.models import Periode, PeriodeSekarang
from .forms import PeriodeForm, PeriodeSekarangForm

# Create your views here.
@admin_required
@require_http_methods(["GET", "POST"])
def create_periode(request):
    if request.method == "POST":
        form = PeriodeForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            
            return redirect(reverse("periode:edit-periode-sekarang"))

    else:
        form = PeriodeForm()
        
    form.fields['univ'].initial = request.user.univ.univ
    form.fields['univ'].label = "univ"
    return render(request, "buat_periode.html", {"form": form})

@admin_required
@require_http_methods(["GET", "POST"])
def edit_periode_sekarang(request):
    if request.method == "POST":
        form = PeriodeSekarangForm(request.POST)
        if form.is_valid():
            new = form.cleaned_data['periode']
            user = request.user
            curr = PeriodeSekarang.objects.filter(univ=user.univ.univ)

            if curr.exists():
                curr.update(periode = new)
            else:
                curr = PeriodeSekarang(periode = new)
                curr.save()
            
            return redirect(reverse("periode:edit-periode-sekarang"))

    else:
        user = request.user
        form = PeriodeSekarangForm()
        queryset = Periode.objects.filter(univ=user.univ.univ).order_by('-tahun_ajaran', 'semester')
        periode_sekarang = PeriodeSekarang.objects.filter(univ=user.univ.univ)
        initial = None if not periode_sekarang.exists() else periode_sekarang.first().periode

    form.fields['periode'].initial = initial
    form.fields['periode'].queryset = queryset
    return render(request, "edit_periode_sekarang.html", {"form": form})

@admin_required
@require_http_methods(["GET", "POST"])
def daftar_ta(request):
    if request.method == 'POST':
        periode_id = request.POST.get("periode")
        periode_terpilih = Periode.objects.get(id=periode_id)
    else:
        periode_terpilih = PeriodeSekarang.objects.first().periode

    daftar_ta = TeachingAssistantProfile.objects.filter(user__univ__univ=request.user.univ.univ)
    daftar_ta_aktif = periode_terpilih.daftar_ta.filter(user__univ__univ=request.user.univ.univ)
    pilihan_periode = Periode.objects.filter(univ=request.user.univ.univ).order_by('-id')

    context = {'daftar_ta': daftar_ta,
               'daftar_ta_aktif': daftar_ta_aktif,
               'periode_terpilih': periode_terpilih,
               'pilihan_periode': pilihan_periode}
    return render(request, 'daftar_ta.html', context)

@require_GET
@admin_required
def assign_ta(request, periode_id):
    user = request.user
    if periode_id is None:
        periode_terpilih = PeriodeSekarang.objects.first().periode
    else:
        periode_terpilih = Periode.objects.get(id=periode_id)

    daftar_ta = TeachingAssistantProfile.objects.filter(user__univ__univ=user.univ.univ)
    daftar_ta_aktif = periode_terpilih.daftar_ta.filter(user__univ__univ=user.univ.univ)
    pilihan_periode = Periode.objects.filter(univ=request.user.univ.univ).order_by('-id')

    context = {'daftar_ta': daftar_ta,
               'daftar_ta_aktif': daftar_ta_aktif,
               'periode_terpilih': periode_terpilih,
               'pilihan_periode': pilihan_periode}
    return render(request, 'assign_ta.html', context)

@require_GET
@admin_required
def activate_ta(request, periode_id, ta_id):
    periode = Periode.objects.get(id = periode_id)
    ta = TeachingAssistantProfile.objects.get(id = ta_id)
    periode.daftar_ta.add(ta)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@require_GET
@admin_required
def deactivate_ta(request, periode_id, ta_id):
    periode = Periode.objects.get(id = periode_id)
    ta = TeachingAssistantProfile.objects.get(id = ta_id)
    periode.daftar_ta.remove(ta)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))