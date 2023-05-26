from django import forms
from .models import Periode, PeriodeSekarang
from django.db.utils import OperationalError, ProgrammingError

class PeriodeSekarangForm(forms.Form):
    try:
        queryset = Periode.objects.all().order_by('-tahun_ajaran', 'semester')
        periode_sekarang = PeriodeSekarang.objects.all()
        initial = None if not periode_sekarang.exists() else periode_sekarang.first().periode

        periode = forms.ModelChoiceField(queryset=queryset, initial=initial, 
                                            widget=forms.Select(attrs={'class': 'form-select'}))
        
    except (OperationalError, ProgrammingError):
        periode = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-select'}))

    

class PeriodeForm(forms.ModelForm):
    class Meta:
        model = Periode
        fields = ['tahun_ajaran', 'semester', 'bulan_mulai', 'bulan_selesai']
        
        widgets = {
            'tahun_ajaran': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 2022/2023'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'bulan_mulai': forms.Select(attrs={'class': 'form-select'}),
            'bulan_selesai': forms.Select(attrs={'class': 'form-select'}),
        }