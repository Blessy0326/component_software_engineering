from django.urls import path
from . import views

urlpatterns = [
    # Basic pages
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('login/confirm/', views.login_logic, name='login_logic'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Search and booking
    path('search_providers/', views.search_providers, name='search_providers'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('book_appointment/<int:provider_id>/', views.book_appointment, name='book_appointment_provider'),
    path('appointment_confirmation/<int:appointment_id>/', views.appointment_confirmation,
         name='appointment_confirmation'),

    # Dashboards
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('provider_dashboard/', views.provider_dashboard, name='provider_dashboard'),

    # Appointment management
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('feedback_rating/<int:appointment_id>/', views.feedback_rating, name='feedback_rating'),

    # Keep compatibility with existing page routing
    path('<slug:page>/', views.page_view, name='page_view'),
    path('<slug:page>.html', views.page_view),
]

# Additional URL patterns for other pages that might be accessed directly
page_names = [
    'appointment_reschedule', 'edit_client_profile', 'edit_provider_profile',
    'manage_appointments_provider', 'manage_reviews', 'manage_users',
    'monitor_bookings', 'notifications_client', 'provider_profile',
    'provider_sync_calendar', 'reporting', 'system_settings', 'upload_content'
]

for name in page_names:
    urlpatterns.append(
        path(f'{name}/', lambda r, name=name: views.page_view(r, name), name=name)
    )