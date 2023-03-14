from django.urls import path
from pengisianLog.views import *

app_name = 'pengisianLog'

urlpatterns = [
    path('daftarLog/<int:userID>', daftarLogTA, name='daftarLogTA'),
    path('daftarLog/', daftarLogEvaluator, name='daftarLogEvaluator'),
]