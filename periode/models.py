import re
from django.db import models
from django.forms import ValidationError
from accounts.models import TeachingAssistantProfile
from itertools import cycle, islice

def tahun_ajaran_validator(data):
    pattern = r"\d{4}/\d{4}"
    if not re.match(pattern, data):
        raise ValidationError(
            'Harus diisi dalam format TAHUN/TAHUN (Contoh: 2023/2024)', code="invalid_format")
    
    tahun_start, tahun_end = data.split('/')
    if int(tahun_start) != int(tahun_end) - 1:
        raise ValidationError(
            'Tahun mulai/selesai tidak valid', code="invalid_time")
    
    return data

# Create your models here.

class Periode(models.Model):
    GANJIL = 'Ganjil'
    GENAP = 'Genap'
    PENDEK = 'Pendek'
    SEMESTER_CHOICES = [
        (GANJIL, 'Ganjil'),
        (GENAP, 'Genap'),
        (PENDEK, 'Pendek'),
    ]

    BULAN_CHOICES = [
        ('JAN','JAN'),
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
        ('DES','DES')
    ]

    tahun_ajaran = models.CharField(max_length=9, validators=[tahun_ajaran_validator])
    semester = models.CharField(
        max_length=6,
        choices=SEMESTER_CHOICES,
        default=GANJIL,
    )

    bulan_mulai = models.CharField(max_length=3,choices=BULAN_CHOICES, default=BULAN_CHOICES[0][0])
    bulan_selesai = models.CharField(max_length=3,choices=BULAN_CHOICES, default=BULAN_CHOICES[4][0])

    daftar_ta = models.ManyToManyField(TeachingAssistantProfile)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tahun_ajaran', 'semester'], name='unique_migration_host_combination'
            )
        ]

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

    def __str__(self):
        return f"{self.tahun_ajaran} {self.semester}"

class PeriodeSekarang(models.Model):
    periode = models.OneToOneField(
        Periode,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.periode)
