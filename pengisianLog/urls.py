from django.urls import path
from pengisianLog.views import form_log_ta, daftar_log_ta, daftar_log_evaluator, detail_log, history_log_ta, edit_log_ta, delete_log_ta

app_name = 'pengisianLog'

urlpatterns = [
    path('mengisi-log/', form_log_ta, name='mengisi_log'),
    path('daftar-log/', daftar_log_ta, name='daftar_log_ta'),
    path('daftar-log-ta/', daftar_log_evaluator, name='daftar_log_evaluator'),
    path('detail-log/<int:id>', detail_log, name='detail_log'),
    path('history-log/<int:id>', history_log_ta, name='history_log'),
    path('edit-log/<int:id>', edit_log_ta, name='edit_log'),
    path('delete-log/<int:id>', delete_log_ta, name='delete_log')
]
