import re
from django.db import models
from django.forms import ValidationError


def validate_tahun_ajaran(data):
    pattern = r"\d{4}/\d{4}"
    if not re.match(pattern, data):
        raise ValidationError(
            'Harus diisi dalam format TAHUN/TAHUN (Contoh: 2023/2024)')
    return data

# Create your models here.

class Periode(models.Model):
    GANJIL = 'Ganjil'
    GENAP = 'Genap'
    SEMESTER_CHOICES = [
        (GANJIL, 'Ganjil'),
        (GENAP, 'Genap'),
    ]

    tahun_ajaran = models.CharField(max_length=9, validators=[validate_tahun_ajaran])
    semester = models.CharField(

        max_length=6,
        choices=SEMESTER_CHOICES,
        default=GANJIL,
    )

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