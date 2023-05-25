from django.urls import path
from accounts.views import profile, fill_profile, edit_profile, dashboard_eval

app_name = 'accounts'

urlpatterns = [
    path('getting-started/', fill_profile, name='fill_profile'),
    path('profile/<int:id>', profile, name='profile'),
    path('profile/<int:id>/edit', edit_profile, name='edit_profile'),
    path('dashboard/', dashboard_eval, name='dashboard_eval'),
]