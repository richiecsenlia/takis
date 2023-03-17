from django.urls import path
from .views import *

app_name = 'pengisianLog'

urlpatterns = [
    path('form-log-kerja/', form_log_TA, name='form-log-kerja'),
    path('daftarLog/', daftarLogTA, name='daftarLogTA'),
    path('daftarLogTA/', daftarLogEvaluator, name='daftarLogEvaluator')
]
