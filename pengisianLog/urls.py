from django.urls import path
from pengisianLog.views import form_log_TA, daftarLogTA, daftarLogEvaluator

app_name = 'pengisianLog'

urlpatterns = [
    path('mengisiLog/', form_log_TA, name='mengisiLog'),
    path('daftarLog/', daftarLogTA, name='daftarLogTA'),
    path('daftarLogTA/', daftarLogEvaluator, name='daftarLogEvaluator')
]
