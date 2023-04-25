from django.urls import path
from .views import *

app_name = 'rekapanLog'

urlpatterns = [
    path('rekap/<str:name>', rekap_page, name='rekapan_log')
]