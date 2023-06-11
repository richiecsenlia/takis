from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.template.defaultfilters import slugify
from django.urls import reverse

def year_validator(data):
    if len(data) != 4:
        raise ValidationError('Harus diisi dalam format tahun (Contoh: 2023)', code="invalid_format")
    
    return data

# Create your models here.
class MataKuliah(models.Model):
    nama = models.CharField(max_length=30)

    def __str__(self):
        return self.nama


class TeachingAssistantProfile(models.Model):
    KONTRAK_CHOICES = [('Part Time','Part Time'),
                       ('Full Time','Full Time')]

    STATUS_CHOICES = [('Lulus S1','Lulus S1'),
                      ('Lulus S2','Lulus S2'),
                      ('Lulus S2 MTI','Lulus S2 MTI')]

    PRODI_CHOICES = [('Ilmu Komputer','Ilmu Komputer'),
                     ('Ilmu Komputer KKI','Ilmu Komputer KKI'),
                     ('Sistem Informasi','Sistem Informasi'),
                     ('Teknologi Informasi','Teknologi Informasi')]
    
    BULAN_CHOICES = [('JAN','JAN'),
                 ('FEB','FEB'),
                 ('MAR','MAR'),
                 ('APR','APR'),
                 ('MEI','MEI'),
                 ('JUN','JUN'),
                 ('JUL','JUL'),
                 ('AGT','AGT'),
                 ('SEP','SEP'),
                 ('OKT','OKT'),
                 ('NOV','NOV'),
                 ('DES','DES')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50, verbose_name='Nama Lengkap')
    kontrak = models.CharField(max_length=20, choices=KONTRAK_CHOICES, verbose_name='Jenis Kontrak')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Status Kemahasiswaan')
    prodi = models.CharField(max_length=30, choices=PRODI_CHOICES, verbose_name='Program Studi')
    daftar_matkul = models.ManyToManyField(MataKuliah)
    bulan_mulai = models.CharField(max_length=3,choices=BULAN_CHOICES,verbose_name='Bulan Mulai')
    tahun_mulai = models.CharField(max_length=4,validators=[year_validator],verbose_name='Tahun Mulai')
    bulan_selesai = models.CharField(max_length=3,choices=BULAN_CHOICES,verbose_name='Bulan Selesai')
    tahun_selesai = models.CharField(max_length=4,validators=[year_validator],verbose_name='Tahun Selesai')
    slug = models.SlugField(unique=True, verbose_name='URL Slug')

    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.slug)])
    
    def bulan_index_generator(self, index_mulai, index_selesai):
        yield index_mulai
        while index_mulai != index_selesai:
            index_mulai += 1
            index_mulai %= 12
            yield index_mulai

    def get_bulan(self):
        list_bulan = [bulan[0] for bulan in self.BULAN_CHOICES]
        index_mulai = list_bulan.index(self.bulan_mulai)
        index_selesai = list_bulan.index(self.bulan_selesai)
        return [list_bulan[i] for i in self.bulan_index_generator(index_mulai, index_selesai)]