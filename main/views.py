from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import date, datetime
from .models import (
    User, ProviderProfile, ClientProfile, Appointment, Review,
    Notification, SystemSettings, ContentUpload, ProviderSearchLog,
    AppointmentAnalytics
)


def index_view(request):
    """Home page view"""
    return render(request, 'index.html')


def login_view(request):
    """Display login form"""
    return render(request, 'login.html')


def login_logic(request):
    """Handle login authentication using database"""
    if request.method == 'POST':
        username = request.POST.get('username')  # This is actually email
        password = request.POST.get('password')
        role = request.POST.get('role', 'client')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user has the correct role
            if user.role == role:
                # Check if provider is approved
                if user.role == 'provider' and not user.is_approved:
                    return render(request, 'login.html', {
                        'error': 'Your provider account is pending approval.'
                    })

                login(request, user)

                # Redirect based on role
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'provider':
                    return redirect('provider_dashboard')
                else:  # client
                    return redirect('client_dashboard')
            else:
                return render(request, 'login.html', {
                    'error': 'Invalid role selected for this account.'
                })
        else:
            return render(request, 'login.html', {
                'error': 'Invalid email or password.'
            })

    return redirect('login')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('index')


def register_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'client')
        terms = request.POST.get('terms')

        # Validate required fields
        if not all([name, email, password, terms]):
            return render(request, 'register.html', {
                'error': 'All fields are required and you must accept terms.'
            })

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'User with this email already exists.'
            })

        try:
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name.split()[0] if name else '',
                last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                role=role,
                is_approved=True if role == 'client' else False  # Clients auto-approved
            )

            # Create profile based on role
            if role == 'client':
                ClientProfile.objects.create(user=user)
            elif role == 'provider':
                specialty = request.POST.get('specialty', '')
                experience = request.POST.get('experience', '')
                location = request.POST.get('location', '')
                availability = request.POST.get('availability', '')

                ProviderProfile.objects.create(
                    user=user,
                    specialty=specialty,
                    experience=experience,
                    location=location,
                    availability=availability
                )

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

        except Exception as e:
            return render(request, 'register.html', {
                'error': f'Registration failed: {str(e)}'
            })

    return render(request, 'register.html')


@login_required
def admin_dashboard(request):
    """Admin dashboard with provider approvals and system settings"""
    if request.user.role != 'admin':
        return redirect('index')

    # Handle provider approval/decline
    if request.method == 'POST':
        provider_id = request.POST.get('provider_id')
        action = request.POST.get('action')

        if provider_id and action:
            try:
                provider = User.objects.get(id=provider_id, role='provider')
                if action == 'approve':
                    provider.is_approved = True
                    provider.save()
                    # Create notification
                    Notification.objects.create(
                        user=provider,
                        notification_type='provider_approved',
                        message='Your provider account has been approved!'
                    )
                    messages.success(request, f'Provider {provider.get_full_name()} approved.')
                elif action == 'decline':
                    provider.delete()
                    messages.success(request, 'Provider application declined.')
            except User.DoesNotExist:
                messages.error(request, 'Provider not found.')

    # Get pending providers
    pending_providers = User.objects.filter(role='provider', is_approved=False)

    # Get system settings
    settings = {}
    for setting in SystemSettings.objects.all():
        settings[setting.setting_key] = setting.setting_value

    context = {
        'pending_providers': pending_providers,
        'settings': settings
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def client_dashboard(request):
    """Client dashboard"""
    if request.user.role != 'client':
        return redirect('index')

    # Get user's appointments
    upcoming_appointments = Appointment.objects.filter(
        client=request.user,
        appointment_date__gte=date.today(),
        status__in=['pending', 'confirmed']
    ).order_by('appointment_date', 'appointment_time')

    # Get notifications
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    )[:5]

    context = {
        'upcoming_appointments': upcoming_appointments,
        'notifications': notifications
    }
    return render(request, 'client_dashboard.html', context)


@login_required
def provider_dashboard(request):
    """Provider dashboard"""
    if request.user.role != 'provider':
        return redirect('index')

    # Handle appointment actions
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')

        if appointment_id and action:
            try:
                appointment = Appointment.objects.get(id=appointment_id, provider=request.user)

                if action == 'accept':
                    appointment.status = 'confirmed'
                    notification_type = 'appointment_confirmed'
                    message = f'Your appointment with {request.user.get_full_name()} has been confirmed.'
                elif action == 'reject':
                    appointment.status = 'cancelled'
                    notification_type = 'appointment_cancelled'
                    message = f'Your appointment with {request.user.get_full_name()} has been cancelled.'
                elif action == 'complete':
                    appointment.status = 'completed'
                    notification_type = 'appointment_reminder'
                    message = f'Your appointment with {request.user.get_full_name()} has been completed. Please leave a review.'

                appointment.save()

                # Create notification for client
                Notification.objects.create(
                    user=appointment.client,
                    notification_type=notification_type,
                    message=message
                )

                messages.success(request, f'Appointment {action}ed successfully.')

            except Appointment.DoesNotExist:
                messages.error(request, 'Appointment not found.')

    # Get provider's appointments
    pending_appointments = Appointment.objects.filter(
        provider=request.user,
        status='pending'
    ).order_by('appointment_date', 'appointment_time')

    confirmed_appointments = Appointment.objects.filter(
        provider=request.user,
        status='confirmed',
        appointment_date__gte=date.today()
    ).order_by('appointment_date', 'appointment_time')

    context = {
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments
    }
    return render(request, 'provider_dashboard.html', context)


def search_providers(request):
    """Search for providers"""
    providers = ProviderProfile.objects.filter(user__is_approved=True)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        specialty = request.POST.get('specialty', '').strip()
        location = request.POST.get('location', '').strip()
        rating = request.POST.get('rating', '').strip()

        # Apply filters
        if name:
            providers = providers.filter(
                Q(user__first_name__icontains=name) |
                Q(user__last_name__icontains=name)
            )

        if specialty:
            providers = providers.filter(specialty__icontains=specialty)

        if location:
            providers = providers.filter(location__icontains=location)

        if rating:
            try:
                min_rating = float(rating)
                providers = providers.filter(rating__gte=min_rating)
            except ValueError:
                pass

        # Log search for analytics
        ProviderSearchLog.objects.create(
            search_name=name,
            search_specialty=specialty,
            search_location=location,
            search_rating=rating,
            searched_by=request.user if request.user.is_authenticated else None,
            results_count=providers.count()
        )

    context = {
        'providers': providers,
        'search_performed': request.method == 'POST'
    }
    return render(request, 'search_providers.html', context)


@login_required
def book_appointment(request, provider_id=None):
    """Book an appointment with a provider"""
    if request.user.role != 'client':
        return redirect('index')

    provider = None
    if provider_id:
        provider = get_object_or_404(User, id=provider_id, role='provider', is_approved=True)

    if request.method == 'POST':
        provider_id = request.POST.get('provider_id') or provider_id
        service = request.POST.get('service')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        if not all([provider_id, service, date_str, time_str]):
            messages.error(request, 'All fields are required.')
        else:
            try:
                provider = User.objects.get(id=provider_id, role='provider', is_approved=True)
                appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                appointment_time = datetime.strptime(time_str, '%H:%M').time()

                # Check if slot is available
                existing = Appointment.objects.filter(
                    provider=provider,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    status__in=['pending', 'confirmed']
                ).exists()

                if existing:
                    messages.error(request, 'This time slot is already booked.')
                else:
                    # Create appointment
                    appointment = Appointment.objects.create(
                        client=request.user,
                        provider=provider,
                        service=service,
                        appointment_date=appointment_date,
                        appointment_time=appointment_time
                    )

                    # Create notification for provider
                    Notification.objects.create(
                        user=provider,
                        notification_type='appointment_reminder',
                        message=f'New appointment request from {request.user.get_full_name()} for {service}.'
                    )

                    return redirect('appointment_confirmation', appointment_id=appointment.id)

            except (User.DoesNotExist, ValueError) as e:
                messages.error(request, f'Error booking appointment: {str(e)}')

    # Get available providers if no specific provider
    if not provider:
        providers = User.objects.filter(role='provider', is_approved=True)
        context = {'providers': providers}
    else:
        context = {'provider': provider}

    return render(request, 'book_appointment.html', context)


@login_required
def appointment_confirmation(request, appointment_id):
    """Show appointment confirmation"""
    appointment = get_object_or_404(Appointment, id=appointment_id, client=request.user)

    context = {
        'appointment': appointment
    }
    return render(request, 'appointment_confirmation.html', context)


@login_required
def manage_bookings(request):
    """Manage client bookings"""
    if request.user.role != 'client':
        return redirect('index')

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')

        if appointment_id and action:
            try:
                appointment = Appointment.objects.get(id=appointment_id, client=request.user)

                if action == 'cancel':
                    appointment.status = 'cancelled'
                    appointment.save()

                    # Notify provider
                    Notification.objects.create(
                        user=appointment.provider,
                        notification_type='appointment_cancelled',
                        message=f'Appointment with {request.user.get_full_name()} has been cancelled.'
                    )

                    messages.success(request, 'Appointment cancelled successfully.')

                elif action == 'reschedule':
                    return redirect('appointment_reschedule', appointment_id=appointment.id)

            except Appointment.DoesNotExist:
                messages.error(request, 'Appointment not found.')

    # Get user's appointments
    appointments = Appointment.objects.filter(
        client=request.user
    ).order_by('-appointment_date', '-appointment_time')

    context = {
        'appointments': appointments
    }
    return render(request, 'manage_bookings.html', context)


@login_required
def feedback_rating(request, appointment_id):
    """Submit feedback and rating for completed appointment"""
    if request.user.role != 'client':
        return redirect('index')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        client=request.user,
        status='completed'
    )

    # Check if review already exists
    if hasattr(appointment, 'review'):
        messages.info(request, 'You have already reviewed this appointment.')
        return redirect('manage_bookings')

    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        rating = request.POST.get('rating')

        if feedback and rating:
            try:
                rating_int = int(rating)
                if 1 <= rating_int <= 5:
                    # Create review
                    Review.objects.create(
                        appointment=appointment,
                        client=request.user,
                        provider=appointment.provider,
                        rating=rating_int,
                        feedback=feedback
                    )

                    # Update provider's average rating
                    provider_profile = appointment.provider.provider_profile
                    avg_rating = Review.objects.filter(
                        provider=appointment.provider
                    ).aggregate(avg_rating=Avg('rating'))['avg_rating']

                    provider_profile.rating = round(avg_rating, 2) if avg_rating else 0
                    provider_profile.save()

                    # Notify provider
                    Notification.objects.create(
                        user=appointment.provider,
                        notification_type='review_received',
                        message=f'You received a new review from {request.user.get_full_name()}.'
                    )

                    messages.success(request, 'Thank you for your feedback!')
                    return redirect('manage_bookings')
                else:
                    messages.error(request, 'Rating must be between 1 and 5.')
            except ValueError:
                messages.error(request, 'Invalid rating value.')
        else:
            messages.error(request, 'Please provide both feedback and rating.')

    context = {
        'appointment': appointment
    }
    return render(request, 'feedback_rating.html', context)


# Helper function for page routing (keeping compatibility with existing URLs)
def page_view(request, page):
    """Generic page view for compatibility"""
    # Map page names to view functions
    view_mapping = {
        'index': index_view,
        'login': login_view,
        'register': register_view,
        'search_providers': search_providers,
        'admin_dashboard': admin_dashboard,
        'client_dashboard': client_dashboard,
        'provider_dashboard': provider_dashboard,
        'manage_bookings': manage_bookings,
    }

    if page in view_mapping:
        return view_mapping[page](request)

    # For other pages, check if user should be logged in
    PROTECTED_PAGES = [
        'admin_dashboard', 'manage_users', 'provider_dashboard',
        'edit_client_profile', 'edit_provider_profile', 'manage_bookings',
        'manage_appointments_provider', 'feedback_rating'
    ]

    if page in PROTECTED_PAGES and not request.user.is_authenticated:
        return redirect('login')

    # Default template rendering
    return render(request, f"{page}.html")