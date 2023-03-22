from django.db import models
from django.contrib.auth.models import User

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

    PRODI_CHOICES = [('IK','Ilmu Komputer'),
                     ('IK KKI','Ilmu Komputer KKI'),
                     ('SI','Sistem Informasi'),
                     ('TI','Teknologi Informasi')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50, verbose_name='Nama Lengkap')
    kontrak = models.CharField(max_length=20, choices=KONTRAK_CHOICES, verbose_name='Jenis Kontrak')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Status Kemahasiswaan')
    prodi = models.CharField(max_length=30, choices=PRODI_CHOICES, verbose_name='Program Studi')
    daftar_matkul = models.ManyToManyField(MataKuliah)

    def __str__(self):
        return self.nama