from django.views.decorators.http import require_http_methods
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
        if form.is_valid():
            form.save()
            return redirect(reverse("periode:edit-periode-sekarang"))

    else:
        form = PeriodeForm()

    return render(request, "buat_periode.html", {"form": form})

@admin_required
@require_http_methods(["GET", "POST"])
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
@require_http_methods(["GET", "POST"])
def daftar_ta(request):
    if request.method == 'POST':
        periode_id = request.POST.get("periode")
        periode_terpilih = Periode.objects.get(id=periode_id)
    else:
        periode_terpilih = PeriodeSekarang.objects.first().periode

    daftar_ta = TeachingAssistantProfile.objects.all()
    daftar_ta_aktif = periode_terpilih.daftar_ta.all()
    pilihan_periode = Periode.objects.all().order_by('-id')

    context = {'daftar_ta': daftar_ta,
               'daftar_ta_aktif': daftar_ta_aktif,
               'periode_terpilih': periode_terpilih,
               'pilihan_periode': pilihan_periode}
    return render(request, 'daftar_ta.html', context)

@admin_required
@require_http_methods(["GET", "POST"])
def assign_ta(request, periode_id):
    if periode_id is None:
        periode_terpilih = PeriodeSekarang.objects.first().periode
    else:
        periode_terpilih = Periode.objects.get(id=periode_id)

    daftar_ta = TeachingAssistantProfile.objects.all()
    daftar_ta_aktif = periode_terpilih.daftar_ta.all()
    pilihan_periode = Periode.objects.all().order_by('-id')

    context = {'daftar_ta': daftar_ta,
               'daftar_ta_aktif': daftar_ta_aktif,
               'periode_terpilih': periode_terpilih,
               'pilihan_periode': pilihan_periode}
    return render(request, 'assign_ta.html', context)

@admin_required
def activate_ta(request, periode_id, ta_id):
    periode = Periode.objects.get(id = periode_id)
    ta = TeachingAssistantProfile.objects.get(id = ta_id)
    periode.daftar_ta.add(ta)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin_required
def deactivate_ta(request, periode_id, ta_id):
    periode = Periode.objects.get(id = periode_id)
    ta = TeachingAssistantProfile.objects.get(id = ta_id)
    periode.daftar_ta.remove(ta)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))