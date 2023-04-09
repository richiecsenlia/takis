from django.urls import path
from pengisianLog.views import form_log_ta, daftar_log_ta, daftar_log_evaluator, detail_log

app_name = 'pengisianLog'

urlpatterns = [
    path('mengisiLog/', form_log_ta, name='mengisiLog'),
    path('daftarLog/', daftar_log_ta, name='daftar_log_ta'),
    path('daftar_log_ta/', daftar_log_evaluator, name='daftar_log_evaluator'),
    path('detail_log/<int:id>', detail_log, name='detail_log')
]
