from django.contrib import admin

from periode.models import Periode, PeriodeSekarang

# Register your models here.
admin.site.register([Periode, PeriodeSekarang])