from django.urls import path
from accounts.views import profile, fill_profile

app_name = 'accounts'

urlpatterns = [
    path('getting-started/', fill_profile, name='fill_profile'),
    path('<slug:slug>/', profile, name='profile'),
]