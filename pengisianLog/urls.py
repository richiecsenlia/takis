from django.urls import path
from . import views

app_name = "pengisian_log"
urlpatterns = [
    path('form-log-kerja/', views.form_log_TA, name='form-log-kerja'),
]
