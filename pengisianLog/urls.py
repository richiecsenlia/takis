from django.urls import path
from pengisianLog.views import *

app_name = 'pengisianLog'

urlpatterns = [
    path('daftarLog/', daftarLog, name='daftarLog'),
]