from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


# Custom User model extending Django's AbstractUser
class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('provider', 'Provider'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    is_approved = models.BooleanField(default=False)  # For provider approval
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Provider Profile Model
class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    specialty = models.CharField(max_length=100, blank=True)
    experience = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    availability = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    calendar_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialty}"


# Client Profile Model
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_appointments')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_appointments')
    service = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration = models.IntegerField(default=30)  # in minutes
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['provider', 'appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.client.username} -> {self.provider.username} on {self.appointment_date} at {self.appointment_time}"


# Feedback/Review Model
class Review(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField()
    reply_text = models.TextField(blank=True)  # Provider's reply
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.username} rated {self.provider.username}: {self.rating}/5"


# Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('appointment_confirmed', 'Appointment Confirmed'),
        ('appointment_cancelled', 'Appointment Cancelled'),
        ('appointment_rescheduled', 'Appointment Rescheduled'),
        ('appointment_reminder', 'Appointment Reminder'),
        ('provider_approved', 'Provider Approved'),
        ('review_received', 'Review Received'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.notification_type}"


# System Settings Model
class SystemSettings(models.Model):
    setting_key = models.CharField(max_length=50, unique=True)
    setting_value = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "System Settings"

    def __str__(self):
        return f"{self.setting_key}: {self.setting_value}"


# Content Upload Model (for prescriptions, FAQs, guides)
class ContentUpload(models.Model):
    CONTENT_TYPES = [
        ('prescription', 'Prescription'),
        ('faq', 'FAQ'),
        ('guide', 'Guide'),
        ('announcement', 'Announcement'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    content_type = models.CharField(max_length=15, choices=CONTENT_TYPES, default='guide')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_content')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.content_type})"


# Provider Search Log Model (for analytics)
class ProviderSearchLog(models.Model):
    search_name = models.CharField(max_length=100, blank=True)
    search_specialty = models.CharField(max_length=100, blank=True)
    search_location = models.CharField(max_length=200, blank=True)
    search_rating = models.CharField(max_length=10, blank=True)
    searched_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    search_timestamp = models.DateTimeField(auto_now_add=True)
    results_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Search by {self.searched_by} on {self.search_timestamp.date()}"


# Appointment Analytics Model (for repoAppointmentrting)
class AppointmentAnalytics(models.Model):
    date = models.DateField(unique=True)
    total_bookings = models.IntegerField(default=0)
    completed_appointments = models.IntegerField(default=0)
    no_shows = models.IntegerField(default=0)
    cancelled_appointments = models.IntegerField(default=0)
    peak_hour = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Appointment Analytics"

    def __str__(self):
        return f"Analytics for {self.date}"