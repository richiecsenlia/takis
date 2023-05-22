import re
from django.db import models
from django.forms import ValidationError
from accounts.models import TeachingAssistantProfile


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

    tahun_ajaran = models.CharField(max_length=9, validators=[tahun_ajaran_validator])
    semester = models.CharField(

        max_length=6,
        choices=SEMESTER_CHOICES,
        default=GANJIL,
    )

    daftar_ta = models.ManyToManyField(TeachingAssistantProfile)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tahun_ajaran', 'semester'], name='unique_migration_host_combination'
            )
        ]

    def __str__(self):
        return f"{self.tahun_ajaran} {self.semester}"

class PeriodeSekarang(models.Model):
    periode = models.OneToOneField(
        Periode,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.periode)
