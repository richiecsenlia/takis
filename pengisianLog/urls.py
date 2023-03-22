from django.urls import path
from .views import *

app_name = 'pengisianLog'

urlpatterns = [
    path('mengisiLog/', form_log_TA, name='mengisiLog'),
    path('daftarLog/', daftarLogTA, name='daftarLogTA'),
    path('daftarLogTA/', daftarLogEvaluator, name='daftarLogEvaluator')
]
