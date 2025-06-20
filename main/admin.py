from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, ProviderProfile, ClientProfile, Appointment, Review,
    Notification, SystemSettings, ContentUpload, ProviderSearchLog,
    AppointmentAnalytics
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_approved', 'is_active')
    list_filter = ('role', 'is_approved', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'is_approved')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'is_approved')
        }),
    )


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    """Provider Profile Admin"""
    list_display = ('user', 'specialty', 'experience', 'location', 'rating')
    list_filter = ('specialty', 'rating')
    search_fields = ('user__first_name', 'user__last_name', 'specialty', 'location')
    ordering = ('-rating',)


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    """Client Profile Admin"""
    list_display = ('user', 'phone_number', 'date_of_birth')
    search_fields = ('user__first_name', 'user__last_name', 'phone_number')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Appointment Admin"""
    list_display = ('client', 'provider', 'service', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'service')
    search_fields = (
    'client__first_name', 'client__last_name', 'provider__first_name', 'provider__last_name', 'service')
    ordering = ('-appointment_date', '-appointment_time')
    date_hierarchy = 'appointment_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin"""
    list_display = ('client', 'provider', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('client__first_name', 'client__last_name', 'provider__first_name', 'provider__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification Admin"""
    list_display = ('user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    """System Settings Admin"""
    list_display = ('setting_key', 'setting_value', 'updated_at', 'updated_by')
    search_fields = ('setting_key', 'setting_value')
    ordering = ('setting_key',)


@admin.register(ContentUpload)
class ContentUploadAdmin(admin.ModelAdmin):
    """Content Upload Admin"""
    list_display = ('title', 'content_type', 'uploaded_by', 'is_active', 'created_at')
    list_filter = ('content_type', 'is_active', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)


@admin.register(ProviderSearchLog)
class ProviderSearchLogAdmin(admin.ModelAdmin):
    """Provider Search Log Admin"""
    list_display = (
    'searched_by', 'search_name', 'search_specialty', 'search_location', 'results_count', 'search_timestamp')
    list_filter = ('search_timestamp', 'search_specialty')
    search_fields = ('search_name', 'search_specialty', 'search_location')
    ordering = ('-search_timestamp',)
    readonly_fields = ('search_timestamp',)


@admin.register(AppointmentAnalytics)
class AppointmentAnalyticsAdmin(admin.ModelAdmin):
    """Appointment Analytics Admin"""
    list_display = (
    'date', 'total_bookings', 'completed_appointments', 'no_shows', 'cancelled_appointments', 'peak_hour')
    list_filter = ('date',)
    ordering = ('-date',)
    date_hierarchy = 'date'