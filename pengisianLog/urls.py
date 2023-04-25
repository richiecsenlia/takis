from django.urls import path
from .views import *

app_name = 'pengisianLog'

urlpatterns = [
    path('mengisiLog/', form_log_TA, name='mengisiLog'),
    path('daftarLog/', daftarLogTA, name='daftarLogTA'),
    path('daftarLogTA/', daftarLogEvaluator, name='daftarLogEvaluator'),
    path('edit_log/<int:id>', edit_log_ta, name='edit_log'),
    path('delete_log/<int:id>', delete_log_ta, name='delete_log')
]
