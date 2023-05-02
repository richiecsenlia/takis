from django.urls import path
from main.views import homepage_handler

app_name = 'main'

urlpatterns = [
    path('', homepage_handler, name='homepage'),
]
