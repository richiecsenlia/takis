from django.urls import path
from pengisianLog.views import form_log_ta, daftar_log_ta, daftar_log_evaluator, detail_log

app_name = 'pengisianLog'

urlpatterns = [
    path('mengisi_log/', form_log_ta, name='mengisiLog'),
    path('daftar_log/', daftar_log_ta, name='daftar_log_ta'),
    path('daftar_log_ta/', daftar_log_evaluator, name='daftar_log_evaluator'),
    path('detail_log/<int:id>', detail_log, name='detail_log')
    path('historyLog/<int:id>', history_log_ta, name='historyLog'),
    path('edit_log/<int:id>', edit_log_ta, name='edit_log'),
    path('delete_log/<int:id>', delete_log_ta, name='delete_log')
]
