
from django.urls import path
from django_cas_ng import views as cas_views
from .views import *
app_name = "authentication"
urlpatterns = [
    path('sso/login/', cas_views.LoginView.as_view(), name='ssologin'),
    path('sso/logout/', cas_views.LogoutView.as_view(), name='ssologout'),
    path('login/',loginHandler,name='login'),
    path('register/',register,name='register'),
    path('change_password/',change_password,name='change_password')
]