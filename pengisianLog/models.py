from django.db import models
from django.contrib.auth.models import User
from periode.models import Periode
from simple_history.models import HistoricalRecords

KATEGORI_CHOICES = [('Dukungan Kuliah Kakak Asuh','Dukungan Kuliah Kakak Asuh'),
                    ('Pengembangan Institusi','Pengembangan Institusi'),
                    ('Penyelenggaraan Kuliah','Penyelenggaraan Kuliah'),
                    ('Persiapan Kuliah','Persiapan Kuliah'),
                    ('Riset dan Pusilkom','Riset dan Pusilkom')]
PERIODE_CHOICES = [ ('Adhoc','Adhoc'),
                    ('Bulanan','Bulanan'),
                    ('Harian','Harian'),
                    ('Semester Kuliah','Semester Kuliah'),
                    ('Sepanjang Kontrak','Sepanjang Kontrak')
                    ]
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


# Create your models here.
class LogTA(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.CharField(max_length=30,choices=KATEGORI_CHOICES)
    jenis_pekerjaan = models.CharField(max_length=20)
    detail_kegiatan = models.CharField(max_length=100)
    pemberi_tugas = models.CharField(max_length=20)
    uraian = models.CharField(max_length=200)
    periode = models.CharField(max_length=20,choices=PERIODE_CHOICES)
    bulan_pengerjaan = models.CharField(max_length=20,choices=BULAN_CHOICES)
    jumlah_rencana_kinerja = models.IntegerField()
    satuan_rencana_kinerja = models.CharField(max_length=20)
    konversi_jam_rencana_kinerja = models.FloatField()
    jumlah_realisasi_kinerja = models.IntegerField(default=0, blank=True, null=True)
    satuan_realisasi_kinerja = models.CharField(default="", max_length=20,blank=True, null=True)
    konversi_jam_realisasi_kinerja = models.FloatField(default=0, blank=True, null=True)
    history = HistoricalRecords()
    periode_log = models.ForeignKey(Periode, on_delete=models.CASCADE, blank=True)