from django import forms
from accounts.models import MataKuliah, TeachingAssistantProfile

class TAProfileForm(forms.ModelForm):
    class Meta:
        model = TeachingAssistantProfile
        fields = ['nama', 'kontrak', 'status', 'prodi', 'bulan_mulai', 'tahun_mulai',
                  'bulan_selesai', 'tahun_selesai', 'daftar_matkul']

        daftar_matkul = forms.ModelMultipleChoiceField(
            queryset=MataKuliah.objects.all()
        )
        widgets = {
            'nama': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Masukkan nama lengkap anda'}
            ),
            'kontrak': forms.Select(
                attrs={'class': 'form-select'},
                choices=TeachingAssistantProfile.KONTRAK_CHOICES,
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'},
                choices=TeachingAssistantProfile.STATUS_CHOICES,
            ),
            'prodi': forms.Select(
                attrs={'class': 'form-select'},
                choices=TeachingAssistantProfile.PRODI_CHOICES,
            ),
            'bulan_mulai': forms.Select(
                attrs={'class': 'form-select'},
                choices=TeachingAssistantProfile.BULAN_CHOICES,
            ),
            'tahun_mulai': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Masukkan tahun mulai kontrak'},
            ),
            'bulan_selesai': forms.Select(
                attrs={'class': 'form-select'},
                choices=TeachingAssistantProfile.BULAN_CHOICES,
            ),
            'tahun_selesai': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Masukkan tahun selesai kontrak'},
            ),
            'daftar_matkul' : forms.CheckboxSelectMultiple()
        }