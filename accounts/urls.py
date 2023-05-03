from django.urls import path
from accounts.views import profile, fill_profile, dashboard_eval

app_name = 'accounts'

urlpatterns = [
    path('getting-started/', fill_profile, name='fill_profile'),
    path('dashboard/', dashboard_eval, name='dashboard_eval'),
    path('<slug:slug>/', profile, name='profile'),
]