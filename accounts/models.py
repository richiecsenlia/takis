from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse

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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50, verbose_name='Nama Lengkap')
    kontrak = models.CharField(max_length=20, choices=KONTRAK_CHOICES, verbose_name='Jenis Kontrak')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Status Kemahasiswaan')
    prodi = models.CharField(max_length=30, choices=PRODI_CHOICES, verbose_name='Program Studi')
    daftar_matkul = models.ManyToManyField(MataKuliah)
    slug = models.SlugField(unique=True, verbose_name='URL Slug')

    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.slug)])