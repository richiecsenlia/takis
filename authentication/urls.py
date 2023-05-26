
from django.urls import path
from django_cas_ng import views as cas_views
from .views import *
app_name = "authentication"
urlpatterns = [
    path('sso/login/', cas_views.LoginView.as_view(), name='ssologin'),
    path('sso/logout/', cas_views.LogoutView.as_view(), name='ssologout'),
    path('login/',login_handler,name='login'),
    path('register/',register,name='register'),
    path('change-password/',change_password,name='change_password'),
    path('not-assign/',not_assign,name="not_assign"),
    path('change-role/',admin_required(change_role),name="change_role"),
    path('change-role/<int:id>/<str:role>',admin_required(update_role),name="update_role"),
]