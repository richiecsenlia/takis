from django.urls import path
from periode.views import create_periode, edit_periode_sekarang, daftar_ta

app_name = 'periode'

urlpatterns = [
    path('buat/', create_periode, name='buat-periode'),
    path('periode-sekarang/', edit_periode_sekarang, name='edit-periode-sekarang'),
    path('daftar-ta/', daftar_ta, name='daftar-ta'),
]
