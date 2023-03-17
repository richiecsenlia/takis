from django.urls import path
from . import views

app_name = 'pengisianLog'

urlpatterns = [
    path('form-log-kerja/', views.form_log_TA, name='form-log-kerja'),
    path('daftarLog/', daftarLogTA, name='daftarLogTA'),
    path('daftarLogTA/', daftarLogEvaluator, name='daftarLogEvaluator'),
]
