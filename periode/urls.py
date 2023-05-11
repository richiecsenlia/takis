from django.urls import path
from periode.views import create_periode, edit_periode_sekarang

app_name = 'periode'

urlpatterns = [
    path('buat/', create_periode, name='buat-periode'),
    path('periode-sekarang/', edit_periode_sekarang, name='edit-periode-sekarang'),
]
