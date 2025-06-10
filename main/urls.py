
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.page_view(r, 'index'), name='index'),
    path('login/', views.login_view, name='login'),
    path('login/confirm/', views.login_logic, name='login_logic'),
    path('logout/', views.logout_view, name='logout'),
]

page_names = [
    'admin_dashboard', 'appointment_confirmation', 'appointment_reschedule',
    'book_appointment', 'client_dashboard', 'edit_client_profile',
    'edit_provider_profile', 'feedback_rating', 'index', 'login',
    'manage_appointments_provider', 'manage_bookings', 'manage_reviews',
    'manage_users', 'monitor_bookings', 'notifications_client',
    'provider_dashboard', 'provider_profile', 'provider_sync_calendar',
    'register', 'reporting', 'search_providers', 'system_settings',
    'upload_content'
]

for name in page_names:
    urlpatterns.append(path(f'{name}/', lambda r, name=name: views.page_view(r, name), name=name))

# Optional: Handle .html URLs
urlpatterns += [
    path('<slug:page>.html', views.page_view),
]
