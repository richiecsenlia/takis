from django.urls import path
from pengisianLog.views import *

app_name = 'pengisianLog'

urlpatterns = [
    path('daftarLog/', daftarLogTA, name='daftarLogTA'),
    path('daftarLogTA/', daftarLogEvaluator, name='daftarLogEvaluator'),
]