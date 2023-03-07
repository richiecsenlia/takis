from django.db import models

JENIS_KONTRAK_CHOICES = [('Part Time','Part Time'),
                         ('Full Time','Full Time')]

STATUS_CHOICES = [('Lulus S1','Lulus S1'),
                  ('Lulus S2','Lulus S2'),
                  ('Lulus S2 MTI','Lulus S2 MTI')]

PRODI_CHOICES = [('Ilmu Komputer','Ilmu Komputer'),
                 ('Ilmu Komputer KKI','Ilmu Komputer KKI'),
                 ('Sistem Informasi','Sistem Informasi')]

# Create your models here.
class UserProfile(models.Model):
    nama_lengkap = models.CharField(max_length=50)
    jenis_kontrak = models.CharField(choices=JENIS_KONTRAK_CHOICES)
    status_kemahasiswaan = models.CharField(choices=STATUS_CHOICES)
    program_studi = models.CharField(choices=PRODI_CHOICES)