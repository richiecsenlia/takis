from django import forms
from accounts.models import MataKuliah, TeachingAssistantProfile

class TAProfileForm(forms.ModelForm):
    class Meta:
        model = TeachingAssistantProfile
        fields = ['nama', 'kontrak', 'status', 'prodi', 'daftar_matkul', 'bulan_mulai', 'bulan_selesai']

        daftar_matkul = forms.ModelMultipleChoiceField(
            queryset=MataKuliah.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama lengkap anda'}),
            'kontrak': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'bulan_mulai': forms.Select(attrs={'class': 'form-select'}),
            'bulan_selesai': forms.Select(attrs={'class': 'form-select'})
        }