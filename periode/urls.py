from django.urls import path
from periode.views import create_periode, edit_periode_sekarang, daftar_ta, assign_ta, activate_ta, deactivate_ta

app_name = 'periode'

urlpatterns = [
    path('buat/', create_periode, name='buat-periode'),
    path('periode-sekarang/', edit_periode_sekarang, name='edit-periode-sekarang'),
    path('daftar-ta/', daftar_ta, name='daftar-ta'),
    path('assign-ta/', assign_ta, {'periode_id': None}, name='assign-ta'),
    path('assign-ta/<int:periode_id>/', assign_ta, name='assign-ta'),
    path('activate/<int:periode_id>/<int:ta_id>/', activate_ta, name='activate-ta'),
    path('deactivate/<int:periode_id>/<int:ta_id>/', deactivate_ta, name='deactivate-ta'),
]
